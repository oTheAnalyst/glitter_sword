CREATE
OR REPLACE TABLE stg.contract_bucket AS SELECT
        *
FROM
        'data/mega_ndjson.json';
CREATE
OR REPLACE TABLE stg.acceptor AS SELECT
        *
FROM
        'data/acceptor_dimension.json';
CREATE
OR REPLACE TABLE stg.acceptor_id AS SELECT
        *
FROM
        'data/acceptor_id.json';
CREATE
OR REPLACE TABLE stg.issuer AS SELECT
        *
FROM
        'data/issuer_records.json';
CREATE
OR REPLACE TABLE stg.dng_contracts_current AS SELECT
        *
FROM
        'data/dng_contracts_current.json';
