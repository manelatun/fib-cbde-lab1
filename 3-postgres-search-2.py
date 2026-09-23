# PostgreSQL, se calcula la distancia en la base de datos mediante procedimientos almacenados

import psycopg2
from scipy.spatial.distance import euclidean, cosine
from prettytable import PrettyTable
import time
import statistics

from lib.do_embeddings import do_embeddings
from config import frases_busqueda, order_by, limit, postgres_config

# https://www.psycopg.org/docs/usage.html
conn = psycopg2.connect(postgres_config)
cur = conn.cursor()

# https://stackoverflow.com/a/34274580
cur.execute("DROP FUNCTION IF EXISTS euclidean_distance(real[], real[], integer)")
cur.execute("""
CREATE OR REPLACE FUNCTION euclidean_distance(l real[], r real[], length integer) RETURNS real AS $$
DECLARE
  s real;
BEGIN
  s := 0;
  FOR i IN 1..length LOOP
    s := s + ((l[i] - r[i])::double precision * (l[i] - r[i]))::double precision;
  END LOOP;
  RETURN sqrt(s);
END;
$$ LANGUAGE plpgsql;
""")

# https://stackoverflow.com/a/56913744
cur.execute("DROP FUNCTION IF EXISTS cosine_distance(real[], real[], integer)")
cur.execute("""
CREATE OR REPLACE FUNCTION cosine_distance(l real[], r real[], length integer) RETURNS real AS $$
DECLARE
  s real;
BEGIN
  s := 1;
  FOR i IN 1..length LOOP
    s := s - (l[i]::double precision * r[i]::double precision);
  END LOOP;
  RETURN s;
END;
$$ LANGUAGE plpgsql;
""")

# el cast a double precision es necesario en la multiplicación, ya que si ni se produce una excepción underflow
# https://www.postgresql.org/docs/current/datatype-numeric.html#DATATYPE-FLOAT

conn.commit()

times = []

# obtiene los embeddings de cada frase de búsqueda
for search in do_embeddings(frases_busqueda)['rows']:

  start = time.perf_counter()

  # obtiene todas las frases y embeddings guardados en PostgreSQL y calcula sus distancias
  cur.execute(f"""
    SELECT
      id,
      euclidean_distance(embedding, %s::real[], 384) AS euclidean_distance,
      cosine_distance(embedding, %s::real[], 384) AS cosine_distance,
      sentence
    FROM sentences
    ORDER BY {order_by}
    LIMIT {limit}
  """, (search['embedding'], search['embedding']))
  rows = cur.fetchall();

  end = time.perf_counter()

  times.append(end - start)

  # output de los resultados de la búsqueda
  print("Search:", search['sentence'])
  print("Time:", end - start)
  table = PrettyTable()
  table.field_names = ["id", "euclidean_distance", "cosine_distance", "sentence"]
  table.align = "l"
  table.add_rows(rows)
  print(table)
  print()

# output de los tiempos de búsqueda
print("Mean:", statistics.mean(times))
print("Median:", statistics.median(times))
print("Standard deviation:", statistics.stdev(times))
print("Min:", min(times))
print("Max:", max(times))
print("Total:", sum(times))
