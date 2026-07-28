import pytest
from app.models.unidad_atencion import UnidadAtencion
from tests.conftest import db_session_maker


async def _create_unidad(**kwargs) -> int:
    async with db_session_maker() as db:
        unidad = UnidadAtencion(
            nombre=kwargs.get("nombre", "Unidad Test"),
            longitude=kwargs.get("longitude", -77.7150),
            latitude=kwargs.get("latitude", 0.8317),
            servicio=kwargs.get("servicio", "DESARROLLO INFANTIL INTEGRAL"),
            region=kwargs.get("region", "Sierra"),
            dpa_despro=kwargs.get("dpa_despro", "CARCHI"),
            dpa_descan=kwargs.get("dpa_descan", "TULCAN"),
            tipo=kwargs.get("tipo", "INTRAMURAL"),
            area=kwargs.get("area", "Urbano"),
            total=kwargs.get("total", 45),
        )
        db.add(unidad)
        await db.commit()
        await db.refresh(unidad)
        return unidad.id


@pytest.mark.anyio
async def test_list_unidades_empty(client):
    response = await client.get("/unidades")
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "FeatureCollection"
    assert data["features"] == []
    assert data["total"] == 0


@pytest.mark.anyio
async def test_list_unidades_returns_geojson(client):
    await _create_unidad()
    response = await client.get("/unidades")
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "FeatureCollection"
    assert len(data["features"]) == 1
    feature = data["features"][0]
    assert feature["type"] == "Feature"
    assert feature["geometry"]["type"] == "Point"
    assert feature["geometry"]["coordinates"] == [-77.7150, 0.8317]
    assert feature["properties"]["nombre"] == "Unidad Test"
    assert "id" in feature


@pytest.mark.anyio
async def test_list_unidades_pagination(client):
    for i in range(5):
        await _create_unidad(nombre=f"Unidad {i}")
    response = await client.get("/unidades?limit=2&offset=0")
    data = response.json()
    assert len(data["features"]) == 2
    assert data["total"] == 5
    assert data["limit"] == 2
    assert data["offset"] == 0

    response2 = await client.get("/unidades?limit=2&offset=2")
    data2 = response2.json()
    assert len(data2["features"]) == 2
    assert data2["offset"] == 2


@pytest.mark.anyio
async def test_list_unidades_filter_region(client):
    await _create_unidad(nombre="Sierra 1", region="Sierra")
    await _create_unidad(nombre="Costa 1", region="Costa")
    response = await client.get("/unidades?region=Sierra")
    data = response.json()
    assert data["total"] == 1
    assert data["features"][0]["properties"]["region"] == "Sierra"


@pytest.mark.anyio
async def test_list_unidades_filter_provincia(client):
    await _create_unidad(nombre="Pichincha", dpa_despro="PICHINCHA")
    await _create_unidad(nombre="Guayas", dpa_despro="GUAYAS")
    response = await client.get("/unidades?provincia=PICHINCHA")
    data = response.json()
    assert data["total"] == 1
    assert data["features"][0]["properties"]["dpa_despro"] == "PICHINCHA"


@pytest.mark.anyio
async def test_list_unidades_filter_nombre(client):
    await _create_unidad(nombre="Centro Salud")
    await _create_unidad(nombre="Hospital General")
    response = await client.get("/unidades?nombre=Centro")
    data = response.json()
    assert data["total"] == 1
    assert "Centro" in data["features"][0]["properties"]["nombre"]


@pytest.mark.anyio
async def test_get_unidad_by_id(client):
    uid = await _create_unidad(nombre="Unidad Individual")
    response = await client.get(f"/unidades/{uid}")
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Unidad Individual"
    assert data["id"] == uid
    assert data["longitude"] == -77.7150


@pytest.mark.anyio
async def test_get_unidad_not_found(client):
    response = await client.get("/unidades/999999")
    assert response.status_code == 404


@pytest.mark.anyio
async def test_health_endpoint(client):
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "version" in data
    assert "database" in data
