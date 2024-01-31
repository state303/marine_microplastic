CREATE TABLE IF NOT EXISTS organization
(
    id   SERIAL
        CONSTRAINT pk__organization__id
            PRIMARY KEY,
    name VARCHAR(255) NOT NULL
        CONSTRAINT uq__organization__name
            UNIQUE
);

CREATE TABLE IF NOT EXISTS doi
(
    id    SERIAL
        CONSTRAINT pk__doi__id
            PRIMARY KEY,
    value VARCHAR(1000) NOT NULL
        CONSTRAINT uq__doi__value
            UNIQUE
);

CREATE TABLE IF NOT EXISTS ocean
(
    id   SERIAL
        CONSTRAINT pk__ocean__id
            PRIMARY KEY,
    name VARCHAR(255) NOT NULL
        CONSTRAINT uq__ocean__name
            UNIQUE
);

CREATE TABLE IF NOT EXISTS region
(
    id   SERIAL
        CONSTRAINT pk__region__id
            PRIMARY KEY,
    name VARCHAR(255) NOT NULL
        CONSTRAINT uq__region__name
            UNIQUE
);

CREATE TABLE IF NOT EXISTS subregion
(
    id   SERIAL
        CONSTRAINT pk__subregion__id
            PRIMARY KEY,
    name VARCHAR(255) NOT NULL
        CONSTRAINT uq__subregion__name
            UNIQUE
);

CREATE TABLE IF NOT EXISTS sample_method
(
    id   SERIAL
        CONSTRAINT pk__sample_method__id
            PRIMARY KEY,
    name VARCHAR(255) NOT NULL
        CONSTRAINT uq__sample_method__name
            UNIQUE
);

CREATE TABLE IF NOT EXISTS unit
(
    id   SERIAL
        CONSTRAINT pk__unit__id
            PRIMARY KEY,
    name VARCHAR(100) NOT NULL
        CONSTRAINT uq__unit__name
            UNIQUE
);

CREATE TABLE IF NOT EXISTS reference
(
    id    SERIAL
        CONSTRAINT pk__reference__id
            PRIMARY KEY,
    title VARCHAR(1000) NOT NULL
        CONSTRAINT uq__reference__title
            UNIQUE
);

CREATE TABLE IF NOT EXISTS measurement
(
    id            SERIAL
        CONSTRAINT pk__measurement__id
            PRIMARY KEY,
    longitude     DOUBLE PRECISION             NOT NULL,
    latitude      DOUBLE PRECISION             NOT NULL,
    ocean         INTEGER
        CONSTRAINT fk__measurement__ocean
            REFERENCES ocean,
    regiON        INTEGER
        CONSTRAINT fk__measurement__region
            REFERENCES region,
    doi           INTEGER
        CONSTRAINT fk__measurement__doi
            REFERENCES doi,
    organization  INTEGER
        CONSTRAINT fk__measurement__organization
            REFERENCES organization,
    subregion     INTEGER
        CONSTRAINT fk__measurement__subregion
            REFERENCES subregion,
    sample_method INTEGER
        CONSTRAINT fk__measurement__sample_method
            REFERENCES sample_method,
    date          DATE                         NOT NULL,
    value         DOUBLE PRECISION DEFAULT 0.0 NOT NULL,
    density_min   DOUBLE PRECISION DEFAULT 0.0,
    density_max   DOUBLE PRECISION DEFAULT 0.0,
    unit          INTEGER                      NOT NULL
        CONSTRAINT fk__measurement__unit
            REFERENCES unit,
    global_id     UUID,
    access_link   VARCHAR(1024),
    reference     INTEGER
        CONSTRAINT fk__measurement__reference
            REFERENCES reference,
    CONSTRAINT uq__measurement__combined
        UNIQUE (latitude, longitude, date)
);

CREATE INDEX idx__measurement__date
    ON measurement (date);

CREATE INDEX idx__measurement__longitude_latitude
    ON measurement (longitude, latitude);

CREATE INDEX idx__measurement__value
    ON measurement (value);