UPDATE star.contracts 
SET dw_is_current = CASE 
  WHEN status = 'outstanding'
  THEN 'current' ELSE 'expired'  END 
                ;
update star.contracts set dw_valid_to = CASE WHEN status = 'finished' THEN date_completed
                                                WHEN status = 'outstanding' THEN date_expired
                                                WHEN status = 'deleted' THEN current_localtimestamp() - INTERVAL '1 day'
                                                END 
                ;
