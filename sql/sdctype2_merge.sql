MERGE INTO master_ducks AS target
USING incoming_ducks AS source
ON target.duck_id = source.duck_id AND target.is_current = true

WHEN MATCHED AND (
       target.duck_name <> source.duck_name OR
       target.breed     <> source.breed     OR
       target.location  <> source.location
) THEN UPDATE SET
    end_date    = CURRENT_DATE - INTERVAL '1 day',
    is_current  = false

WHEN NOT MATCHED BY SOURCE AND target.is_current = true THEN UPDATE SET
    end_date    = CURRENT_DATE - INTERVAL '1 day',
    is_current  = false

WHEN NOT MATCHED BY TARGET THEN INSERT (
    record_id, duck_id, duck_name, breed, location,
    begin_date, end_date, is_current
) VALUES (
    nextval('duck_record_seq'),
    source.duck_id, source.duck_name, source.breed, source.location,
    source.begin_date, source.end_date, source.is_current
)

RETURNING merge_action, *;
