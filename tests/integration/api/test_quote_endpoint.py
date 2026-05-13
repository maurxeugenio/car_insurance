import pytest


BASE_URL = "/api/v1/quotes"


@pytest.fixture
def payload():
    return {
        "broker_fee": 50.0,
        "car": {
            "make": "Mitsubishi",
            "model": "ASX",
            "value": 100000.0,
            "year": 2015,
        },
        "deductible_percentage": 0.10,
    }


class TestPostQuote:
    async def test_returns_200(self, client, payload):
        response = await client.post(BASE_URL, json=payload)
        assert response.status_code == 200

    async def test_response_contains_required_fields(self, client, payload):
        response = await client.post(BASE_URL, json=payload)
        data = response.json()
        assert "applied_rate" in data
        assert "calculated_premium" in data
        assert "policy_limit" in data
        assert "deductible_value" in data

    async def test_echoes_car_details(self, client, payload):
        response = await client.post(BASE_URL, json=payload)
        data = response.json()
        assert data["car"]["make"] == "Mitsubishi"
        assert data["car"]["model"] == "ASX"
        assert data["car"]["value"] == 100000.0
        assert data["car"]["year"] == 2015

    async def test_applied_rate_is_positive(self, client, payload):
        response = await client.post(BASE_URL, json=payload)
        assert response.json()["applied_rate"] > 0

    async def test_calculated_premium_is_positive(self, client, payload):
        response = await client.post(BASE_URL, json=payload)
        assert response.json()["calculated_premium"] > 0

    async def test_policy_limit_is_less_than_car_value(self, client, payload):
        response = await client.post(BASE_URL, json=payload)
        data = response.json()
        assert data["policy_limit"] < payload["car"]["value"]

    async def test_with_registration_location(self, client, payload):
        payload["registration_location"] = {
            "city": "São Paulo",
            "country": "Brazil",
            "state": "SP",
        }
        response = await client.post(BASE_URL, json=payload)
        assert response.status_code == 200
        assert "applied_rate" in response.json()

    async def test_missing_car_returns_422(self, client):
        response = await client.post(BASE_URL, json={
            "broker_fee": 50.0,
            "deductible_percentage": 0.10,
        })
        assert response.status_code == 422

    async def test_invalid_deductible_above_one_returns_422(self, client, payload):
        payload["deductible_percentage"] = 1.5
        response = await client.post(BASE_URL, json=payload)
        assert response.status_code == 422

    async def test_negative_broker_fee_returns_422(self, client, payload):
        payload["broker_fee"] = -10.0
        response = await client.post(BASE_URL, json=payload)
        assert response.status_code == 422

    async def test_negative_car_value_returns_422(self, client, payload):
        payload["car"]["value"] = -1.0
        response = await client.post(BASE_URL, json=payload)
        assert response.status_code == 422


class TestHealthEndpoint:
    async def test_health_returns_200(self, client):
        response = await client.get("/health")
        assert response.status_code == 200

    async def test_health_returns_ok_status(self, client):
        response = await client.get("/health")
        assert response.json()["status"] == "It's ok and aqui é galo!"