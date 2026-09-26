# PostgreSQL, inserción en una única transacción con precisión simple

import psycopg2
import statistics
import json
import time

from config import postgres_config

# https://www.psycopg.org/docs/usage.html
conn = psycopg2.connect(postgres_config)
cur = conn.cursor()
cur.execute("""
DROP TABLE IF EXISTS sentences CASCADE;
DROP TABLE IF EXISTS embeddings CASCADE;
""")
cur.execute("""
CREATE TABLE sentences (
  id INTEGER PRIMARY KEY,
  sentence TEXT
)
""")
cur.execute("""
CREATE TABLE embeddings (
  sentence_id INTEGER PRIMARY KEY references sentences(id),
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
print("Subiendo frases a PostgreSQL")

sentences_insert_times = []

# inserta las frases del dataset en PostgreSQL
for row in result['rows']:
  start = time.perf_counter()
  cur.execute("INSERT INTO sentences (id, sentence) VALUES (%s, %s)", (row['id'], row['sentence']))
  end = time.perf_counter()
  sentences_insert_times.append(end - start)

start = time.perf_counter()
conn.commit()
end = time.perf_counter()
sentences_commit_time = end - start


print("Subiendo embeddings a PostgreSQL")

embeddings_insert_times = []

# inserta los embeddings del dataset en PostgreSQL
for row in result['rows']:
  start = time.perf_counter()
  cur.execute("INSERT INTO embeddings (sentence_id, embedding) VALUES (%s, %s)", (row['id'], row['embedding']))
  end = time.perf_counter()
  embeddings_insert_times.append(end - start)

start = time.perf_counter()
conn.commit()
end = time.perf_counter()
embeddings_commit_time = end - start

cur.close()
conn.close()

# output de los tiempos de inserción
print("Insercion de las frases: ")
print("Mean:", statistics.mean(sentences_insert_times))
print("Median:", statistics.median(sentences_insert_times))
print("Standard deviation:", statistics.stdev(sentences_insert_times))
print("Min:", min(sentences_insert_times))
print("Max:", max(sentences_insert_times))
print("Total:", sum(sentences_insert_times))
print("+Commit:", sentences_commit_time)

print("Insercion de los embeddings: ")
print("Mean:", statistics.mean(embeddings_insert_times))
print("Median:", statistics.median(embeddings_insert_times))
print("Standard deviation:", statistics.stdev(embeddings_insert_times))
print("Min:", min(embeddings_insert_times))
print("Max:", max(embeddings_insert_times))
print("Total:", sum(embeddings_insert_times))
print("+Commit:", embeddings_commit_time)
