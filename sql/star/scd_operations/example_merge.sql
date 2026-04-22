MERGE INTO star.contract AS target
USING stg.dng_contract AS source
ON target.contract_id = source.contract_id AND target.dw_is_current = 'current'

WHEN MATCHED AND (
  target.date_completed <> source.date_completed OR
  target.date_accepted <> source.date_accepted OR
  target.acceptor_id <> source.acceptor_id OR
  target.status  <> source.status
  ) THEN UPDATE SET 
    dw_valid_to = CASE WHEN target.status = 'deleted' THEN current_localtimestamp() - INTERVAL '1 day'
     WHEN source.date_completed IS NOT NULL THEN source.date_completed
     WHEN source.date_completed IS NULL THEN source.date_expired
     END,
    dw_is_current = 'expired'

WHEN NOT MATCHED BY SOURCE AND target.dw_is_current = 'current' THEN UPDATE SET 
    dw_valid_to = CASE WHEN target.status = 'deleted' THEN current_localtimestamp() - INTERVAL '1 day'
     WHEN source.date_completed IS NOT NULL THEN source.date_completed
     WHEN source.date_completed IS NULL THEN source.date_expired
     END,
    dw_is_current = 'expired'

 WHEN NOT MATCHED BY TARGET THEN INSERT BY NAME 


RETURNING merge_action, *;
