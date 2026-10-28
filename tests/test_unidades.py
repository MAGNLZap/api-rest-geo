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


@pytest.mark.asyncio
async def test_list_unidades_empty(client):
    response = await client.get("/unidades")
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "FeatureCollection"
    assert data["features"] == []
    assert data["total"] == 0


@pytest.mark.asyncio
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


@pytest.mark.asyncio
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


@pytest.mark.asyncio
async def test_list_unidades_filter_region(client):
    await _create_unidad(nombre="Sierra 1", region="Sierra")
    await _create_unidad(nombre="Costa 1", region="Costa")
    response = await client.get("/unidades?region=Sierra")
    data = response.json()
    assert data["total"] == 1
    assert data["features"][0]["properties"]["region"] == "Sierra"


@pytest.mark.asyncio
async def test_list_unidades_filter_provincia(client):
    await _create_unidad(nombre="Pichincha", dpa_despro="PICHINCHA")
    await _create_unidad(nombre="Guayas", dpa_despro="GUAYAS")
    response = await client.get("/unidades?provincia=PICHINCHA")
    data = response.json()
    assert data["total"] == 1
    assert data["features"][0]["properties"]["dpa_despro"] == "PICHINCHA"


@pytest.mark.asyncio
async def test_list_unidades_filter_nombre(client):
    await _create_unidad(nombre="Centro Salud")
    await _create_unidad(nombre="Hospital General")
    response = await client.get("/unidades?nombre=Centro")
    data = response.json()
    assert data["total"] == 1
    assert "Centro" in data["features"][0]["properties"]["nombre"]


@pytest.mark.asyncio
async def test_get_unidad_by_id(client):
    uid = await _create_unidad(nombre="Unidad Individual")
    response = await client.get(f"/unidades/{uid}")
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "Feature"
    assert data["geometry"]["type"] == "Point"
    assert data["geometry"]["coordinates"] == [-77.7150, 0.8317]
    assert data["properties"]["nombre"] == "Unidad Individual"
    assert data["properties"]["id"] == uid
    assert data["id"] == str(uid)


@pytest.mark.asyncio
async def test_get_unidad_not_found(client):
    response = await client.get("/unidades/999999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_health_endpoint(client):
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "version" in data
    assert "database" in data


@pytest.mark.asyncio
async def test_list_unidades_raw_empty(client):
    response = await client.get("/unidades/raw")
    assert response.status_code == 200
    data = response.json()
    assert data["data"] == []
    assert data["total"] == 0


@pytest.mark.asyncio
async def test_list_unidades_raw_returns_flat_json(client):
    await _create_unidad()
    response = await client.get("/unidades/raw")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert len(data["data"]) == 1
    item = data["data"][0]
    assert item["nombre"] == "Unidad Test"
    assert item["longitude"] == -77.7150
    assert item["latitude"] == 0.8317
    assert "type" not in item
    assert "geometry" not in item
    assert "properties" not in item


@pytest.mark.asyncio
async def test_list_unidades_raw_pagination(client):
    for i in range(5):
        await _create_unidad(nombre=f"Unidad {i}")
    response = await client.get("/unidades/raw?limit=2&offset=0")
    data = response.json()
    assert len(data["data"]) == 2
    assert data["total"] == 5
    assert data["limit"] == 2
    assert data["offset"] == 0


@pytest.mark.asyncio
async def test_list_unidades_raw_with_filters(client):
    await _create_unidad(nombre="Sierra Raw", region="Sierra")
    await _create_unidad(nombre="Costa Raw", region="Costa")
    response = await client.get("/unidades/raw?region=Sierra")
    data = response.json()
    assert data["total"] == 1
    assert data["data"][0]["region"] == "Sierra"


@pytest.mark.asyncio
async def test_get_unidad_raw_by_id(client):
    uid = await _create_unidad(nombre="Unidad Raw Individual")
    response = await client.get(f"/unidades/{uid}/raw")
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Unidad Raw Individual"
    assert data["id"] == uid
    assert data["longitude"] == -77.7150
    assert data["latitude"] == 0.8317
    assert "type" not in data
    assert "geometry" not in data


@pytest.mark.asyncio
async def test_get_unidad_raw_not_found(client):
    response = await client.get("/unidades/999999/raw")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_unidades_bbox_filter(client):
    await _create_unidad(nombre="Dentro", longitude=-77.71, latitude=0.83)
    await _create_unidad(nombre="Fuera", longitude=-80.00, latitude=-2.00)
    response = await client.get("/unidades?bbox=-78,0,-77,1")
    data = response.json()
    assert data["total"] == 1
    assert data["features"][0]["properties"]["nombre"] == "Dentro"


@pytest.mark.asyncio
async def test_list_unidades_limit_zero_returns_all(client):
    for i in range(5):
        await _create_unidad(nombre=f"Unidad {i}")
    response = await client.get("/unidades?limit=0")
    data = response.json()
    assert len(data["features"]) == 5
    assert data["total"] == 5
    assert data["limit"] == 0


@pytest.mark.asyncio
async def test_list_unidades_bbox_with_limit_zero(client):
    await _create_unidad(nombre="Dentro A", longitude=-77.71, latitude=0.83)
    await _create_unidad(nombre="Dentro B", longitude=-77.72, latitude=0.84)
    await _create_unidad(nombre="Fuera", longitude=-80.00, latitude=-2.00)
    response = await client.get("/unidades?bbox=-78,0,-77,1&limit=0")
    data = response.json()
    assert data["total"] == 2
    assert len(data["features"]) == 2
    nombres = [f["properties"]["nombre"] for f in data["features"]]
    assert "Dentro A" in nombres
    assert "Dentro B" in nombres


@pytest.mark.asyncio
async def test_list_unidades_raw_bbox_filter(client):
    await _create_unidad(nombre="Raw Dentro", longitude=-77.71, latitude=0.83)
    await _create_unidad(nombre="Raw Fuera", longitude=-80.00, latitude=-2.00)
    response = await client.get("/unidades/raw?bbox=-78,0,-77,1")
    data = response.json()
    assert data["total"] == 1
    assert data["data"][0]["nombre"] == "Raw Dentro"


@pytest.mark.asyncio
async def test_list_unidades_raw_limit_zero(client):
    for i in range(5):
        await _create_unidad(nombre=f"Raw {i}")
    response = await client.get("/unidades/raw?limit=0")
    data = response.json()
    assert len(data["data"]) == 5
    assert data["limit"] == 0
