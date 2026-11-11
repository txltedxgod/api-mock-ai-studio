from fastapi.testclient import TestClient

from mock_ai.api import app
from mock_ai.generator import APIMockGenerator

client = TestClient(app)


def test_mock_gen() -> None:
    g = APIMockGenerator()
    res = g.generate_mock_for_schema("UserProfile")
    assert "mock_data" in res
    assert res["schema"] == "UserProfile"
    assert res["mock_data"]["id"].startswith("use_")


def test_mock_gen_determinism_and_schemas() -> None:
    g = APIMockGenerator()
    a = g.generate_mock_for_schema("Order", count=2, seed=42)
    b = g.generate_mock_for_schema("Order", count=2, seed=42)
    assert a == b
    assert len(a["items"]) == 2
    assert "amount_cents" in a["mock_data"]


def test_mock_api_endpoints() -> None:
    assert client.get("/health").json() == {"status": "ok"}

    resp = client.get("/api/v1/mock/ProductItem?count=3&seed=7")
    assert resp.status_code == 200
    body = resp.json()
    assert len(body["items"]) == 3
    assert "sku" in body["mock_data"]

    bad_count = client.get("/api/v1/mock/UserProfile?count=0")
    assert bad_count.status_code == 422

    blank_schema = client.get("/api/v1/mock/%20%20")
    assert blank_schema.status_code == 400
