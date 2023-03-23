DROP TABLE if exists urls CASCADE;
DROP TABLE if exists url_checks CASCADE;


CREATE TABLE urls (
    id              bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name            varchar(255) UNIQUE NOT NULL,
    created_at      date NOT NULL
);


CREATE TABLE url_checks (
    id              bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    url_id          bigint NOT NULL REFERENCES urls (id),
    status_code     smallint NOT NULL,
    h1              varchar(255),
    title           varchar(255),
    description     varchar(255),
    created_at      date NOT NULL
);
