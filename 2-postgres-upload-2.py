# PostgreSQL, inserción en una única transacción con precisión doble

import psycopg2
import statistics
import json
import time

# https://www.psycopg.org/docs/usage.html
conn = psycopg2.connect(dbname="cbde", user="cbde", password="cbde")
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS sentences CASCADE")
cur.execute("""
CREATE TABLE sentences (
  id INTEGER PRIMARY KEY,
  sentence TEXT,
  embedding DOUBLE PRECISION[]
)
""")

print("Cargando embeddings.json")

# carga los embeddings desde el fichero ("simulamos" que los estamos generando)
start = time.perf_counter()
with open('embeddings.json', 'r') as f:
  result = json.load(f)
end = time.perf_counter()
load_time = end - start

print(f"{result['count']} embeddings, generados originalmente en {result['elapsed']} (Cargados en {load_time})")
print()
print("Subiendo a PostgreSQL")

insert_times = []

# inserta los embedddings de cada frase del dataset en PostgreSQL
for row in result['rows']:
  start = time.perf_counter()
  cur.execute("INSERT INTO sentences (id, sentence, embedding) VALUES (%s, %s, %s)", (row['id'], row['sentence'], row['embedding']))
  end = time.perf_counter()
  insert_times.append(end - start)

start = time.perf_counter()
conn.commit()
end = time.perf_counter()
commit_time = end - start

cur.close()
conn.close()

# output de los tiempos de inserción
print("Mean:", statistics.mean(insert_times))
print("Median:", statistics.median(insert_times))
print("Standard deviation:", statistics.stdev(insert_times))
print("Min:", min(insert_times))
print("Max:", max(insert_times))
print("Total:", sum(insert_times))
print("+Commit:", commit_time)
