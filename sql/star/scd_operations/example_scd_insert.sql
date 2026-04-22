INSERT INTO star.contract BY NAME (
SELECT source.*,
       source.date_issued AS dw_valid_from,
  CASE WHEN target.status = 'deleted' THEN current_localtimestamp() - INTERVAL '1 day'
     WHEN source.date_completed IS NOT NULL THEN source.date_completed
     WHEN source.date_completed IS NULL THEN source.date_expired
     END as dw_valid_to, 
    'current' AS dw_is_current
FROM stg.dng_contract as source 
INNER JOIN star.contract as target 
  ON source.contract_id = target.contract_id
    WHERE target.dw_is_current = 'expired' 
      AND source.import_id = 8
      AND target.dw_valid_to::date < today() 
  );

  SELECT status, dw_is_current, contract_id
  FROM star.contract;
