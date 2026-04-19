create or replace table stg.contract_bucket as
                select * from 'data/mega_ndjson.json';
