DROP TABLE IF EXISTS stg.stg_imports;

CREATE TABLE stg.stg_imports (
   import_id BIGINT NOT NULL DEFAULT nextval('log'),
   import_dt TIMESTAMP PRIMARY KEY DEFAULT current_localtimestamp(),
   source_name VARCHAR,
   original_file_path VARCHAR,
   bucket_uri VARCHAR,
   md5_checksum VARCHAR
);

