plat = 'md:glitter_sword'

reset star_table:
	@echo "reset star tabe using backup table"
	duckdb $(plat) < sql/star/scd_operations/reset_star.sql

scd_merg_test:
	@echo "ingested new data into database from stagging table into types 2 table"
	duckdb $(plat) < sql/star/scd_operations/example_merge.sql
	duckdb $(plat) < sql/star/scd_operations/example_scd_insert.sql



scd_ui_test:
	@echo "ingested new data into database from stagging into SCD type 2 table"
	duckdb $(plat) < sql/star/scd_operations/crud_scdupdate.sql
	duckdb $(plat) < sql/star/scd_operations/scdinsert.sql

ingest_stg_layer:
	@echo "ingest data into json"
	python ./python/Ingestion/ds_current_contract.py
	python ./python/Ingestion/ds_bucket_contracts.py
	python ./python/Ingestion/ds_corprate_identity.py
	duckdb $(plat) < sql/stg/imports/stg_ingestion.sql
