#!/usr/bin/env python3
"""
MCP Demo with DuckDB
Simple demonstration of Model Context Protocol with database operations.
"""

import duckdb

def main():
    """Main demo function"""
    con = duckdb.connect('sample.db')
    print('Connected to sample.db')
    
    query = '''
    SELECT instance_name, cost_per_hour
    FROM aws_instances
    ORDER BY cost_per_hour DESC
    LIMIT 3
    '''
    results = con.execute(query).fetchall()
    print('Top 3 highest cost AWS instances:')
    for name, cost in results:
        print(f'- {name}: ${cost}/hour')

if __name__ == '__main__':
    main()