import hashlib

import httpx

from src.domain.ports.gis_port import IGISPort
from src.domain.value_objects.address import Address
from src.domain.value_objects.rate import Rate

_NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
_USER_AGENT = "car-insurance-simulator/0.1.0"


class GISAdapter(IGISPort):
    """
    Geographic risk adapter — fully async.

    Strategy (in order):
      1. GIS_SERVICE_URL set       → proprietary GIS API
      2. GIS_SERVICE_URL empty     → OpenStreetMap Nominatim (free, no key)
      3. Any network failure       → deterministic hash fallback
    """

    def __init__(
        self,
        max_adjustment: float = 0.02,
        service_url: str = "",
    ) -> None:
        self._max_adjustment = max_adjustment
        self._service_url = service_url

    async def adjust_rate(self, address: Address, rate: Rate) -> Rate:
        if self._service_url:
            adjustment = await self._fetch_proprietary(address)
        else:
            adjustment = await self._fetch_osm_adjustment(address)

        return rate.adjusted(adjustment)

    # ── OpenStreetMap Nominatim ───────────────────────────────────────────────

    async def _fetch_osm_adjustment(self, address: Address) -> float:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    _NOMINATIM_URL,
                    params={
                        "city": address.city,
                        "country": address.country,
                        "format": "json",
                        "limit": 1,
                        "state": address.state,
                    },
                    headers={"User-Agent": _USER_AGENT},
                    timeout=5.0,
                )
                response.raise_for_status()
                results = response.json()

            if not results:
                return self._hash_fallback(address)

            lat = float(results[0]["lat"])
            lon = float(results[0]["lon"])
            return self._coords_to_adjustment(lat, lon)

        except Exception:
            return self._hash_fallback(address)

    def _coords_to_adjustment(self, lat: float, lon: float) -> float:
        """
        Maps lat/lon to a risk adjustment in [-max_adjustment, +max_adjustment].

          - Absolute latitude normalised 0–90 → 0.0 (poles) to 1.0 (equator)
          - Longitude used as a secondary dispersion factor
          - Both blended and mapped to [-max, +max]
        """
        lat_score = (90 - abs(lat)) / 90
        lon_factor = (abs(lon) % 90) / 90
        blended = (lat_score * 0.7) + (lon_factor * 0.3)
        normalized = (blended * 2) - 1
        return round(normalized * self._max_adjustment, 6)

    # ── Proprietary GIS (optional) ────────────────────────────────────────────

    async def _fetch_proprietary(self, address: Address) -> float:
        """
        Calls a proprietary GIS API.
        Expected response: { "adjustment": 0.012 }
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    self._service_url,
                    params={
                        "city": address.city,
                        "country": address.country,
                        "state": address.state,
                    },
                    timeout=3.0,
                )
                response.raise_for_status()
                raw = float(response.json()["adjustment"])
                return max(-self._max_adjustment, min(self._max_adjustment, raw))

        except Exception:
            return self._hash_fallback(address)

    # ── Hash fallback ─────────────────────────────────────────────────────────

    def _hash_fallback(self, address: Address) -> float:
        """Deterministic risk score — no network required."""
        raw = f"{address.city}:{address.state}:{address.country}".lower()
        digest = hashlib.sha256(raw.encode()).hexdigest()
        score = int(digest[:4], 16) / 65535.0
        normalized = (score * 2) - 1
        return round(normalized * self._max_adjustment, 6)