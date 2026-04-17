INSERT INTO star.target (
acceptor_id ,
assignee_id ,
availability ,
collateral ,
contract_id ,
date_accepted ,
date_completed ,
date_expired ,
date_issued ,
days_to_complete ,
end_location_id ,
for_corporation ,
issuer_corporation_id ,
issuer_id ,
price ,
reward ,
start_location_id ,
status ,
title ,
"types",
volume,
import_id,
record_id 
)
SELECT 
acceptor_id ,
assignee_id ,
availability ,
collateral ,
contract_id ,
date_accepted ,
date_completed ,
date_expired ,
date_issued ,
days_to_complete ,
end_location_id ,
for_corporation ,
issuer_corporation_id ,
issuer_id ,
price ,
reward ,
start_location_id ,
status ,
title ,
"types",
volume,
import_id,
record_id 
FROM stg.dng_contracts as source
INNER JOIN star.target as target
  ON source.contract_id = target.contract_id
WHEN target.status =  'finished'


