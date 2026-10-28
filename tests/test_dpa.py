import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("level", "expected", "properties"),
    [
        ("provincias", 24, {"id", "name"}),
        ("cantones", 222, {"id", "name", "province_id"}),
        ("parroquias", 1048, {"id", "name", "canton_id", "province_id"}),
    ],
)
async def test_dpa_geojson(
    client: AsyncClient,
    level: str,
    expected: int,
    properties: set[str],
) -> None:
    response = await client.get(f"/dpa/{level}")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/geo+json")
    assert response.headers["content-encoding"] == "gzip"

    data = response.json()
    assert data["type"] == "FeatureCollection"
    assert len(data["features"]) == expected
    assert set(data["features"][0]["properties"]) == properties
    assert data["features"][0]["geometry"]["type"] == "MultiPolygon"


@pytest.mark.asyncio
async def test_dpa_supports_identity_encoding(client: AsyncClient) -> None:
    response = await client.get("/dpa/provincias", headers={"Accept-Encoding": "identity"})

    assert response.status_code == 200
    assert "content-encoding" not in response.headers
    assert response.headers["vary"] == "Accept-Encoding"
    assert len(response.json()["features"]) == 24
