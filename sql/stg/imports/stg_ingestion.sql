CREATE
OR REPLACE TABLE stg.contract_bucket AS 
FROM
        'data/mega_ndjson.json';
CREATE
OR REPLACE TABLE stg.issuer AS 
FROM
        'data/issuer_records.json';
CREATE
OR REPLACE TABLE stg.dng_contracts_current AS 
FROM
        'data/dng_contracts_current.json';
CREATE
OR REPLACE TABLE stg.acceptor_records AS 
FROM
        'data/acceptor_dimension.json'
