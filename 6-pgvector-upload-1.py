# PostgreSQL, inserción en una única transacción con tipo de datos vector (de pgVector)

import psycopg2
import statistics
import json
import time

from config import postgres_config

# https://www.psycopg.org/docs/usage.html
conn = psycopg2.connect(postgres_config)
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS sentences_pgvector CASCADE")
cur.execute("DROP TABLE IF EXISTS embeddings_pgvector CASCADE")
cur.execute("""
CREATE TABLE sentences_pgvector (
  id INTEGER PRIMARY KEY,
  sentence TEXT
)
""")
cur.execute("""
CREATE TABLE embeddings_pgvector (
  sentence_id INTEGER PRIMARY KEY references sentences_pgvector(id),
  embedding vector(384)
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

sentence_insert_times = []

# inserta las frase del dataset en PostgreSQL
for row in result['rows']:
  start = time.perf_counter()
  cur.execute("INSERT INTO sentences_pgvector (id, sentence) VALUES (%s, %s)", (row['id'], row['sentence']))
  end = time.perf_counter()
  sentence_insert_times.append(end - start)

start = time.perf_counter()
conn.commit()
end = time.perf_counter()
sentence_commit_time = end - start


print("Subiendo embeddings a PostgreSQL")

embeddings_insert_times = []

# inserta las frase del dataset en PostgreSQL
for row in result['rows']:
  start = time.perf_counter()
  cur.execute("INSERT INTO embeddings_pgvector (sentence_id, embedding) VALUES (%s, %s)", (row['id'], row['embedding']))
  end = time.perf_counter()
  embeddings_insert_times.append(end - start)

start = time.perf_counter()
conn.commit()
end = time.perf_counter()
embeddings_commit_time = end - start


cur.close()
conn.close()

# output de los tiempos de inserción
print("Tiempo de insercion de las frases: ")
print("Mean:", statistics.mean(sentence_insert_times))
print("Median:", statistics.median(sentence_insert_times))
print("Standard deviation:", statistics.stdev(sentence_insert_times))
print("Min:", min(sentence_insert_times))
print("Max:", max(sentence_insert_times))
print("Total:", sum(sentence_insert_times))
print("+Commit:", sentence_commit_time)

print("Tiempo de insercion de los embeddings: ")
print("Mean:", statistics.mean(embeddings_insert_times))
print("Median:", statistics.median(embeddings_insert_times))
print("Standard deviation:", statistics.stdev(embeddings_insert_times))
print("Min:", min(embeddings_insert_times))
print("Max:", max(embeddings_insert_times))
print("Total:", sum(embeddings_insert_times))
print("+Commit:", embeddings_commit_time)
