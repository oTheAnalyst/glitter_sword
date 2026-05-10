SELECT title, count(*) as n 
FROM star.contract
WHERE dw_is_current = 'current'
and status = 'outstanding'
group by title
order by n desc;



-- Step 1: Expire changed records
UPDATE star.contract 
SET dw_is_current = 'expired'
WHERE dw_is_current = 'current'
  AND contract_id IN (
    SELECT source.contract_id
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
    )
);

SELECT title, count(*) as n 
FROM star.contract
WHERE dw_is_current = 'current'
and status = 'outstanding'
group by title
order by n desc;
