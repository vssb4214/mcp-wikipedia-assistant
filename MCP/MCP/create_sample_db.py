import duckdb

# initiate the database
con = duckdb.connect('sample.db')

# sample table
con.execute('''
CREATE TABLE IF NOT EXISTS aws_instances (
    id INTEGER PRIMARY KEY,
    instance_name VARCHAR,
    cost_per_hour DOUBLE
)
''')

# sample data
con.execute('DELETE FROM aws_instances')  # clear existing data
con.executemany('''
INSERT INTO aws_instances (id, instance_name, cost_per_hour) VALUES (?, ?, ?)
''', [
    (1, 'm5.large', 0.096),
    (2, 'c5.xlarge', 0.17),
    (3, 'r5.2xlarge', 0.504),
    (4, 't3.micro', 0.0104),
    (5, 'p3.2xlarge', 3.06),
    (6, 'g4dn.xlarge', 0.526),
])

print('Sample database created as sample.db') 