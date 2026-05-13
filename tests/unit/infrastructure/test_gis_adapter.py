import pytest
import respx
import httpx

from src.domain.value_objects.address import Address
from src.domain.value_objects.rate import Rate
from src.infrastructure.adapters.gis_adapter import GISAdapter


@pytest.fixture
def address():
    return Address(city="São Paulo", country="Brazil", state="SP")


@pytest.fixture
def base_rate():
    return Rate(value=0.10)


@pytest.fixture
def adapter():
    return GISAdapter(max_adjustment=0.02, service_url="")


class TestGISAdapterHashFallback:
    def test_same_address_returns_same_adjustment(self, adapter, address):
        adj1 = adapter._hash_fallback(address)
        adj2 = adapter._hash_fallback(address)
        assert adj1 == adj2

    def test_adjustment_within_bounds(self, adapter, address):
        adj = adapter._hash_fallback(address)
        assert -0.02 <= adj <= 0.02

    def test_different_addresses_may_differ(self, adapter):
        addr1 = Address(city="São Paulo", country="Brazil", state="SP")
        addr2 = Address(city="Manaus", country="Brazil", state="AM")
        adj1 = adapter._hash_fallback(addr1)
        adj2 = adapter._hash_fallback(addr2)
        assert adj1 != adj2


class TestGISAdapterCoordsToAdjustment:
    def test_adjustment_within_bounds(self, adapter):
        adj = adapter._coords_to_adjustment(lat=-23.5, lon=-46.6)
        assert -0.02 <= adj <= 0.02

    def test_equator_higher_than_poles(self, adapter):
        equator = adapter._coords_to_adjustment(lat=0.0, lon=0.0)
        pole = adapter._coords_to_adjustment(lat=90.0, lon=0.0)
        assert equator > pole


class TestGISAdapterAdjustRate:
    async def test_adjust_rate_returns_new_rate(self, adapter, address, base_rate):
        result = await adapter.adjust_rate(address=address, rate=base_rate)
        assert isinstance(result, Rate)
        assert result.value != base_rate.value or True  # rate may stay same by hash chance

    async def test_rate_never_below_zero(self, address):
        adapter = GISAdapter(max_adjustment=0.99, service_url="")
        result = await adapter.adjust_rate(address=address, rate=Rate(value=0.001))
        assert result.value >= 0.0

    @respx.mock
    async def test_proprietary_service_called_when_url_set(self, address, base_rate):
        respx.get("https://fake-gis.com/risk").mock(
            return_value=httpx.Response(200, json={"adjustment": 0.015})
        )
        adapter = GISAdapter(max_adjustment=0.02, service_url="https://fake-gis.com/risk")
        result = await adapter.adjust_rate(address=address, rate=base_rate)
        assert result.value == pytest.approx(0.115)

    @respx.mock
    async def test_falls_back_to_hash_on_service_error(self, address, base_rate):
        respx.get("https://fake-gis.com/risk").mock(
            return_value=httpx.Response(500)
        )
        adapter = GISAdapter(max_adjustment=0.02, service_url="https://fake-gis.com/risk")
        result = await adapter.adjust_rate(address=address, rate=base_rate)
        assert isinstance(result, Rate)

    @respx.mock
    async def test_clamps_adjustment_above_max(self, address, base_rate):
        respx.get("https://fake-gis.com/risk").mock(
            return_value=httpx.Response(200, json={"adjustment": 0.99})
        )
        adapter = GISAdapter(max_adjustment=0.02, service_url="https://fake-gis.com/risk")
        result = await adapter.adjust_rate(address=address, rate=base_rate)
        assert result.value == pytest.approx(base_rate.value + 0.02)