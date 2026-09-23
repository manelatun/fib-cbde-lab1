import psycopg2
import statistics

# https://www.psycopg.org/docs/usage.html
conn = psycopg2.connect(dbname="cbde", user="cbde", password="cbde")
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS sentences CASCADE")
cur.execute("""
CREATE TABLE sentences (
  id INTEGER PRIMARY KEY,
  sentence TEXT,
  embeddings REAL[]
)
""")
