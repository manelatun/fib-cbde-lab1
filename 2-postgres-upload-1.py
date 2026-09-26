# PostgreSQL, inserción uno a uno con precisión doble

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

sentences_times = []

# inserta las frases del dataset en PostgreSQL
for row in result['rows']:
  start = time.perf_counter()
  cur.execute("INSERT INTO sentences (id, sentence) VALUES (%s, %s)", (row['id'], row['sentence']))
  conn.commit()
  end = time.perf_counter()
  sentences_times += [end - start]

print("Subiendo embeddings a PostgreSQL")

embeddings_times = []

# inserta los embedddings de cada frase del dataset en PostgreSQL
for row in result['rows']:
  start = time.perf_counter()
  cur.execute("INSERT INTO embeddings (sentence_id, embedding) VALUES (%s, %s)", (row['id'], row['embedding']))
  conn.commit()
  end = time.perf_counter()
  embeddings_times += [end - start]

cur.close()
conn.close()

# output de los tiempos de inserción
print("Tiempo de insercion de las frases:")
print("Mean:", statistics.mean(sentences_times))
print("Median:", statistics.median(sentences_times))
print("Standard deviation:", statistics.stdev(sentences_times))
print("Min:", min(sentences_times))
print("Max:", max(sentences_times))
print("Total:", sum(sentences_times))

print("Tiempo de insercion de los embeddings:")
print("Mean:", statistics.mean(embeddings_times))
print("Median:", statistics.median(embeddings_times))
print("Standard deviation:", statistics.stdev(embeddings_times))
print("Min:", min(embeddings_times))
print("Max:", max(embeddings_times))
print("Total:", sum(embeddings_times))
