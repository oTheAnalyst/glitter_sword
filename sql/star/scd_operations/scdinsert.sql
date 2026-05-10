-- Step 2: Insert new current versions
INSERT INTO star.contract (
    contract_id,
    date_completed,
    date_accepted,
    acceptor_id,
    status,
    dw_is_current,
    dw_valid_from,
    dw_valid_to
)
SELECT 
    source.contract_id,
    source.date_completed,
    source.date_accepted,
    source.acceptor_id,
    source.status,
    'current',
    CURRENT_TIMESTAMP,
    NULL
FROM stg.test32 AS source
WHERE EXISTS (
    SELECT 1 
    FROM star.contract AS target
    WHERE target.contract_id = source.contract_id
      AND target.dw_is_current = 'current'
      AND (
        target.date_completed IS DISTINCT FROM source.date_completed OR
        target.date_accepted IS DISTINCT FROM source.date_accepted OR
        target.acceptor_id IS DISTINCT FROM source.acceptor_id OR
        target.status IS DISTINCT FROM source.status
    )
);

SELECT title, count(*) as n_total_contracts 
FROM star.contract
group by title
order by n desc;


SELECT title, count(*) as n 
FROM star.contract
WHERE dw_is_current = 'current'
and status = 'outstanding'
group by title
order by n desc;
