from typing import Any, Literal

from pydantic import BaseModel, Field


class Point(BaseModel):
    type: Literal["Point"] = "Point"
    coordinates: tuple[float, float] = Field(
        ..., description="[longitude, latitude]"
    )


class LineString(BaseModel):
    type: Literal["LineString"] = "LineString"
    coordinates: list[tuple[float, float]] = Field(
        ..., min_length=2, description="Lista de [longitude, latitude]"
    )


class Polygon(BaseModel):
    type: Literal["Polygon"] = "Polygon"
    coordinates: list[list[tuple[float, float]]] = Field(
        ..., min_length=1, description="Anillo exterior + anillos interiores"
    )


class MultiPoint(BaseModel):
    type: Literal["MultiPoint"] = "MultiPoint"
    coordinates: list[tuple[float, float]]


class MultiLineString(BaseModel):
    type: Literal["MultiLineString"] = "MultiLineString"
    coordinates: list[list[tuple[float, float]]]


class MultiPolygon(BaseModel):
    type: Literal["MultiPolygon"] = "MultiPolygon"
    coordinates: list[list[list[tuple[float, float]]]]


Geometry = Point | LineString | Polygon | MultiPoint | MultiLineString | MultiPolygon


class Feature(BaseModel):
    type: Literal["Feature"] = "Feature"
    geometry: Geometry = Field(..., description="Geometría del elemento")
    properties: dict[str, Any] = Field(default_factory=dict, description="Propiedades arbitrarias")
    id: str | int | None = None


class FeatureCollection(BaseModel):
    type: Literal["FeatureCollection"] = "FeatureCollection"
    features: list[Feature] = Field(default_factory=list)
