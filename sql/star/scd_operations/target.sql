MERGE INTO star.target AS target
USING stg.dng_contract AS source
ON target.contract_id = source.contract_id AND target.status = 'outstanding'


WHEN MATCHED AND (
  target.acceptor_id <> source.acceptor_id OR
  target.date_completed <> source.date_completed
  AND target.date_completed IS NOT NULL
  ) THEN UPDATE SET 
      status = 'finished'

WHEN NOT MATCHED BY SOURCE AND target.status = 'outstanding' 
  AND target.date_completed IS NOT NULL THEN UPDATE SET 
      status = 'finished'


WHEN NOT MATCHED BY TARGET THEN INSERT (
assignee_id,
availability,
collateral,
contract_id,
date_accepted,
date_completed,
date_expired,
date_issued,
days_to_complete,
end_location_id,
for_corporation,
issuer_corporation_id,
issuer_id,
price,
reward,
start_location_id,
status,
title,
"type",
volume,
import_id
) VALUES (
source.assignee_id,
source.availability,
source.collateral,
source.contract_id,
source.date_accepted,
source.date_completed,
source.date_expired,
source.date_issued,
source.days_to_complete,
source.end_location_id,
source.for_corporation,
source.issuer_corporation_id,
source.issuer_id,
source.price,
source.reward,
source.start_location_id,
source.status,
source.title,
source."type",
source.volume,
source.import_id
  )

RETURNING merge_action, *;



