INSERT INTO stg.dng_contract BY NAME 
(SELECT * FROM 'data/dng_contracts_current.json');
