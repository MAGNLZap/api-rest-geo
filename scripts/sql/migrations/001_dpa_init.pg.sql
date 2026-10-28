CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE IF NOT EXISTS provinces (
    id   TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    geom geometry(MultiPolygon, 4326) NOT NULL
);

CREATE TABLE IF NOT EXISTS cantons (
    id          TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    province_id TEXT NOT NULL,
    geom        geometry(MultiPolygon, 4326) NOT NULL,
    CONSTRAINT fk_cantons_province FOREIGN KEY (province_id) REFERENCES provinces (id)
);

CREATE TABLE IF NOT EXISTS parishes (
    id          TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    canton_id   TEXT NOT NULL,
    province_id TEXT NOT NULL,
    geom        geometry(MultiPolygon, 4326) NOT NULL,
    CONSTRAINT fk_parishes_canton FOREIGN KEY (canton_id) REFERENCES cantons (id),
    CONSTRAINT fk_parishes_province FOREIGN KEY (province_id) REFERENCES provinces (id)
);

CREATE INDEX IF NOT EXISTS idx_provinces_geom ON provinces USING GIST (geom);
CREATE INDEX IF NOT EXISTS idx_cantons_geom ON cantons USING GIST (geom);
CREATE INDEX IF NOT EXISTS idx_parishes_geom ON parishes USING GIST (geom);
CREATE INDEX IF NOT EXISTS idx_cantons_province ON cantons (province_id);
CREATE INDEX IF NOT EXISTS idx_parishes_canton ON parishes (canton_id);
CREATE INDEX IF NOT EXISTS idx_parishes_province ON parishes (province_id);
