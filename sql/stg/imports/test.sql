SELECT *
FROM stg.contract_bucket as contract_bucket
LEFT JOIN stg.types as types
ON contract_bucket.type_id = types._key;
