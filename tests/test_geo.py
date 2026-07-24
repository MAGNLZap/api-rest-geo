import pytest
from tests.conftest import db_session_maker


@pytest.mark.anyio
async def test_list_points_empty(client):
    response = await client.get("/geo/points")
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "FeatureCollection"
    assert data["features"] == []


@pytest.mark.anyio
async def test_list_points_with_data(client):
    async with db_session_maker() as db:
        from app.models.point import GeoPoint

        point = GeoPoint(
            name="Punto Test",
            description="Un punto de prueba",
            longitude=-73.9857,
            latitude=40.7484,
            category="test",
        )
        db.add(point)
        await db.commit()

    response = await client.get("/geo/points")
    assert response.status_code == 200
    data = response.json()
    assert len(data["features"]) == 1
    feature = data["features"][0]
    assert feature["geometry"]["type"] == "Point"
    assert feature["geometry"]["coordinates"] == [-73.9857, 40.7484]
    assert feature["properties"]["name"] == "Punto Test"


@pytest.mark.anyio
async def test_get_point_not_found(client):
    response = await client.get("/geo/points/999")
    assert response.status_code == 404


@pytest.mark.anyio
async def test_get_point(client):
    async with db_session_maker() as db:
        from app.models.point import GeoPoint

        point = GeoPoint(
            name="Punto Uno",
            longitude=-73.9857,
            latitude=40.7484,
        )
        db.add(point)
        await db.commit()
        await db.refresh(point)
        point_id = point.id

    response = await client.get(f"/geo/points/{point_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "Feature"
    assert data["geometry"]["type"] == "Point"
    assert data["properties"]["name"] == "Punto Uno"
