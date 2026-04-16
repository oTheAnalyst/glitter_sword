INSERT INTO master_ducks (
    record_id, duck_id, duck_name, breed, location,
    begin_date, end_date, is_current
)
SELECT
    nextval('duck_record_seq'),
    source.duck_id,
    source.duck_name,
    source.breed,
    source.location,
    CURRENT_DATE AS begin_date,
    NULL AS end_date,
    true AS is_current
FROM incoming_ducks AS source
INNER JOIN master_ducks AS target
    ON source.duck_id = target.duck_id
WHERE target.is_current = false
  AND target.end_date = CURRENT_DATE - INTERVAL '1 day';
