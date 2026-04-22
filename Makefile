plat = 'md:glitter_sword'

scd_operation_test:
	@echo "ingested new data into database from stagging table into normalized table"
	duckdb $(plat) < sql/star/scd_operations/example_merge.sql
	duckdb $(plat) < sql/star/scd_operations/example_scd_insert.sql
