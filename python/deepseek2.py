#!/usr/bi/env python3
"""
Convert JSON files to DuckDB-readable formats.
Supports: JSON arrays, JSON lines, and nested JSON objects.
"""

import json
import sys
import argparse
import pandas as pd
from pathlib import Path
from typing import Union, List, Dict, Any

def flatten_json(data: Any, parent_key: str = '', sep: str = '_') -> Any:
    """
    Flatten nested JSON structures.
    
    Args:
        data: JSON data (dict, list, or primitive)
        parent_key: Key from parent level
        sep: Separator for nested keys
    
    Returns:
        Flattened data structure
    """
    if isinstance(data, dict):
        items = {}
        for k, v in data.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.update(flatten_json(v, new_key, sep=sep))
            elif isinstance(v, list):
                # Convert list to JSON string for DuckDB compatibility
                items[new_key] = json.dumps(v) if v else None
            else:
                items[new_key] = v
        return items
    elif isinstance(data, list):
        return [flatten_json(item, parent_key, sep) for item in data]
    else:
        return data

def convert_json_to_duckdb_format(input_file: str, output_file: str = None, 
                                  format_type: str = 'parquet', flatten: bool = True):
    """
    Convert JSON file to DuckDB-readable format.
    
    Args:
        input_file: Path to input JSON file
        output_file: Path to output file (auto-generated if None)
        format_type: Output format ('parquet', 'csv', 'jsonl')
        flatten: Whether to flatten nested structures
    """
    
    # Read JSON file
    print(f"Reading JSON file: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Convert to DataFrame
    if isinstance(data, list):
        print(f"Found JSON array with {len(data)} items")
        if flatten:
            df = pd.DataFrame([flatten_json(item) for item in data])
        else:
            df = pd.DataFrame(data)
    elif isinstance(data, dict):
        print(f"Found JSON object with {len(data)} keys")
        if flatten:
            df = pd.DataFrame([flatten_json(data)])
        else:
            # Check if it's a record-oriented dict (list of dicts)
            if all(isinstance(v, list) for v in data.values()):
                df = pd.DataFrame(data)
            else:
                df = pd.DataFrame([data])
    else:
        raise ValueError("JSON root must be an object or array")
    
    # Generate output filename if not provided
    if output_file is None:
        input_path = Path(input_file)
        if format_type == 'parquet':
            output_file = input_path.stem + '.parquet'
        elif format_type == 'csv':
            output_file = input_path.stem + '.csv'
        elif format_type == 'jsonl':
            output_file = input_path.stem + '.jsonl'
        else:
            output_file = input_path.stem + '_converted.json'
    
    # Save in requested format
    print(f"Converting to {format_type.upper()}...")
    print(f"Data shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    
    if format_type == 'parquet':
        df.to_parquet(output_file, index=False)
    elif format_type == 'csv':
        df.to_csv(output_file, index=False)
    elif format_type == 'jsonl':
        df.to_json(output_file, orient='records', lines=True)
    else:
        raise ValueError(f"Unsupported format: {format_type}")
    
    print(f"Successfully saved to: {output_file}")
    return output_file

def create_duckdb_schema(input_file: str, table_name: str = 'my_table'):
    """
    Generate DuckDB CREATE TABLE statement from JSON structure.
    
    Args:
        input_file: Path to JSON file
        table_name: Name for the DuckDB table
    
    Returns:
        SQL CREATE TABLE statement
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Get sample record
    if isinstance(data, list) and len(data) > 0:
        sample = data[0]
    elif isinstance(data, dict):
        sample = data
    else:
        return f"-- Could not infer schema from {input_file}"
    
    # Map Python types to DuckDB types
    type_mapping = {
        str: 'VARCHAR',
        int: 'BIGINT',
        float: 'DOUBLE',
        bool: 'BOOLEAN',
        list: 'JSON',
        dict: 'JSON',
        type(None): 'VARCHAR'
    }
    
    columns = []
    for key, value in sample.items():
        if isinstance(value, list):
            # Check if list contains only primitive types
            if all(isinstance(x, (str, int, float, bool, type(None))) for x in value):
                duckdb_type = f"{type_mapping[type(value[0]) if value else str]}[]"
            else:
                duckdb_type = 'JSON'
        else:
            duckdb_type = type_mapping.get(type(value), 'VARCHAR')
        
        columns.append(f'    "{key}" {duckdb_type}')
    
    create_stmt = f"CREATE TABLE {table_name} (\n" + ",\n".join(columns) + "\n);"
    return create_stmt

def main():
    parser = argparse.ArgumentParser(
        description='Convert JSON files to DuckDB-readable formats',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s data.json
  %(prog)s data.json -o output.parquet -f parquet
  %(prog)s data.json --no-flatten -f csv
  %(prog)s data.json --schema --table-name my_table
        """
    )
    
    parser.add_argument('input', help='Input JSON file path')
    parser.add_argument('-o', '--output', help='Output file path')
    parser.add_argument('-f', '--format', choices=['parquet', 'csv', 'jsonl'], 
                       default='parquet', help='Output format (default: parquet)')
    parser.add_argument('--no-flatten', action='store_true', 
                       help='Do not flatten nested JSON structures')
    parser.add_argument('--schema', action='store_true',
                       help='Generate DuckDB CREATE TABLE schema instead of converting')
    parser.add_argument('--table-name', default='my_table',
                       help='Table name for schema generation (default: my_table)')
    
    args = parser.parse_args()
    
    # Check if input file exists
    if not Path(args.input).exists():
        print(f"Error: Input file '{args.input}' not found", file=sys.stderr)
        sys.exit(1)
    
    try:
        if args.schema:
            # Generate and print schema
            schema = create_duckdb_schema(args.input, args.table_name)
            print("\nDuckDB Schema:")
            print("=" * 50)
            print(schema)
            print("\nTo use with DuckDB:")
            print("  import duckdb")
            print(f"  conn = duckdb.connect(':memory:')")
            print(f"  conn.execute('''{schema}''')")
            print(f"  conn.execute(\"COPY {args.table_name} FROM 'your_file.{args.format}'\")\n")
        else:
            # Convert file
            output_file = convert_json_to_duckdb_format(
                args.input, 
                args.output, 
                args.format, 
                flatten=not args.no_flatten
            )
            
            # Print DuckDB usage example
            print("\n" + "=" * 50)
            print("DuckDB Usage Example:")
            print("=" * 50)
            print(f"""
import duckdb

# Connect to DuckDB
conn = duckdb.connect(':memory:')

# Read the {args.format.upper()} file directly
df = conn.execute("SELECT * FROM read_{args.format}('{output_file}')").fetchdf()

# Or for Parquet files:
# df = conn.execute("SELECT * FROM read_parquet('{output_file}')").fetchdf()

# Query the data
print(df.head())
            """.strip())
            
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON file - {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
