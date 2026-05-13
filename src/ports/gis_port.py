import hashlib

from src.domain.ports.gis_port import IGISPort
from src.domain.value_objects.address import Address
from src.domain.value_objects.rate import Rate


class GISAdapter(IGISPort):
    """
    Geographic risk adapter.

    When no external GIS service URL is configured, falls back to a
    deterministic local risk score derived from the address hash.
    This ensures consistent results for the same address without
    requiring an external dependency in development.

    Risk adjustment range: -max_adjustment to +max_adjustment (default ±2%).
    """

    def __init__(
        self,
        max_adjustment: float = 0.02,
        service_url: str = "",
    ) -> None:
        self._max_adjustment = max_adjustment
        self._service_url = service_url

    def adjust_rate(self, address: Address, rate: Rate) -> Rate:
        if self._service_url:
            adjustment = self._fetch_remote_adjustment(address)
        else:
            adjustment = self._local_adjustment(address)

        return rate.adjusted(adjustment)

    # ── private ──────────────────────────────────────────────────────────────

    def _local_adjustment(self, address: Address) -> float:
        """
        Derives a deterministic risk score from the address string.

        Uses SHA-256 so the same city/state/country always produces
        the same adjustment — useful for testing and dev without
        a real GIS service.
        """
        raw = f"{address.city}:{address.state}:{address.country}".lower()
        digest = hashlib.sha256(raw.encode()).hexdigest()

        # Map the first 4 hex chars (0–65535) to a -1.0 to +1.0 range
        score = int(digest[:4], 16) / 65535.0  # 0.0 → 1.0
        normalized = (score * 2) - 1           # -1.0 → +1.0

        return round(normalized * self._max_adjustment, 6)

    def _fetch_remote_adjustment(self, address: Address) -> float:
        """
        Calls an external GIS service to retrieve the risk adjustment.

        Expected response format:
            { "adjustment": 0.012 }

        The adjustment must be within [-max_adjustment, +max_adjustment].
        Any value outside this range is clamped for safety.
        """
        import httpx

        try:
            response = httpx.get(
                self._service_url,
                params={
                    "city": address.city,
                    "country": address.country,
                    "state": address.state,
                },
                timeout=3.0,
            )
            response.raise_for_status()
            data = response.json()
            raw = float(data["adjustment"])
            return max(-self._max_adjustment, min(self._max_adjustment, raw))

        except Exception:
            # GIS is non-critical — fall back to local on any failure
            return self._local_adjustment(address)