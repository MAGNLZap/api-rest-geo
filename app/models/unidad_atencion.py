from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class UnidadAtencion(Base):
    __tablename__ = "unidades_atencion"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    zon_plan: Mapped[str | None] = mapped_column(String(255))
    dis_sen: Mapped[str | None] = mapped_column(String(50))
    uni_des: Mapped[str | None] = mapped_column(String(500))
    dpa_despro: Mapped[str | None] = mapped_column(String(100))
    dpa_prov: Mapped[str | None] = mapped_column(String(10))
    dpa_descan: Mapped[str | None] = mapped_column(String(100))
    dpa_can: Mapped[str | None] = mapped_column(String(10))
    dpa_despar: Mapped[str | None] = mapped_column(String(100))
    dpa_par: Mapped[str | None] = mapped_column(String(10))
    region: Mapped[str | None] = mapped_column(String(50))
    co_siimdh: Mapped[int | None] = mapped_column(Integer)
    nombre: Mapped[str] = mapped_column(String(500))
    servicio: Mapped[str | None] = mapped_column(String(255))
    mod: Mapped[str | None] = mapped_column(String(255))
    mod_abv: Mapped[str | None] = mapped_column(String(100))
    dir: Mapped[str | None] = mapped_column(String(500))
    ref: Mapped[str | None] = mapped_column(String(500))
    ruc: Mapped[str | None] = mapped_column(String(20))
    tipo_admin: Mapped[str | None] = mapped_column(String(100))
    cooperante: Mapped[str | None] = mapped_column(String(255))
    tipo: Mapped[str | None] = mapped_column(String(50))
    hombre: Mapped[int | None] = mapped_column(Integer)
    mujer: Mapped[int | None] = mapped_column(Integer)
    total: Mapped[int | None] = mapped_column(Integer)
    area: Mapped[str | None] = mapped_column(String(50))
    asis_prom: Mapped[float | None] = mapped_column(Float)
    asistencia: Mapped[int | None] = mapped_column(Integer)
    rs18: Mapped[int | None] = mapped_column(Integer)
    no_rs18: Mapped[int | None] = mapped_column(Integer)
    ext_pob18: Mapped[int | None] = mapped_column(Integer)
    pob18: Mapped[int | None] = mapped_column(Integer)
    no_pob18: Mapped[int | None] = mapped_column(Integer)
    rs25: Mapped[int | None] = mapped_column(Integer)
    no_rs25: Mapped[int | None] = mapped_column(Integer)
    ext_pob25: Mapped[int | None] = mapped_column(Integer)
    pob25: Mapped[int | None] = mapped_column(Integer)
    no_pob25: Mapped[int | None] = mapped_column(Integer)
    x: Mapped[float | None] = mapped_column(Float)
    y: Mapped[float | None] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    latitude: Mapped[float] = mapped_column(Float)
    link_ubi: Mapped[str | None] = mapped_column(String(500))
    corte: Mapped[str | None] = mapped_column(String(100))

    def __repr__(self) -> str:
        return f"<UnidadAtencion(id={self.id}, nombre='{self.nombre}', lon={self.longitude}, lat={self.latitude})>"
