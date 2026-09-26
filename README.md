1. Para generar los embeddings del dataset bookcorpus hay que ejecutar `1-embeddings-bookcorpus-colab.ipynb` o `1-embeddings-bookcorpus-local.py` que guardan el resultado en `embeddings.json`. El repositorio ya contiene un fichero `embeddings.json` con los embeddings de las primeras 10.000 frases de bookcorpus.

2. Modifica el fichero `config/postgresql.py` con la información de conexión a la base de datos.

   Ejemplo de como crear la base de datos:

   ```sh
   sudo -u postgres psql -U postgres -d postgres
   ```
   ```sql
   -- Crea el usuario y la base de datos
   CREATE ROLE cbde WITH LOGIN PASSWORD 'cbde';
   CREATE DATABASE cbde WITH OWNER cbde;
   -- Configura pgVector para más adelante
   \connect cbde
   CREATE EXTENSION vector;
   ```

3. Modifica el fichero `config.py` con los datos de acceso a la base de datos

## PostgreSQL

### Upload

`2-postgres-upload-1.py` - Inserción uno a uno con precisión doble
```
Mean: 0.00231111077904643
Median: 0.0021759055016445927
Standard deviation: 0.0015962606958873859
Min: 0.0019384240004001185
Max: 0.08599822800169932
Total: 23.111107790464303
```

```
Tiempo de insercion de las frases:
Mean: 0.001151759961996504
Median: 0.001057226500051911
Standard deviation: 0.00038744559227839613
Min: 0.000585695999689051
Max: 0.0035506690001056995
Total: 1.151759961996504

Tiempo de insercion de los embeddings:
Mean: 0.0019528759649915628
Median: 0.0018490329998712696
Standard deviation: 0.00048043450917845695
Min: 0.0013545570000133011
Max: 0.007506477999868366
Total: 1.9528759649915628
```

`2-postgres-upload-2.py` - Inserción en una única transacción con precisión doble
```
Mean: 0.0018722217488437308
Median: 0.001820840498112375
Standard deviation: 0.0007943038868382593
Min: 0.0016950850040302612
Max: 0.05532023399427999
Total: 18.72221748843731
+Commit: 0.008220557996537536
```

```
Tiempo de insercion de las frases:
Mean: 8.073956400403404e-05
Median: 7.600200001434132e-05
Standard deviation: 4.822509207712381e-05
Min: 4.239100007907837e-05
Max: 0.000563206999686372
Total: 0.08073956400403404
+Commit: 0.0037710970000262023

Tiempo de insercion de los embeddings:
Mean: 0.000864730579992738
Median: 0.0008045575000323879
Standard deviation: 0.00023201281845818827
Min: 0.0006426020004255406
Max: 0.003437836000102834
Total: 0.8647305799927381
+Commit: 0.0011187039999640547
```

`2-postgres-upload-3.py` - Inserción en una única transacción con precisión simple
```
Mean: 0.001576021734972892
Median: 0.0015084985025168862
Standard deviation: 0.0007259174817578377
Min: 0.0014100800035521388
Max: 0.0591532999969786
Total: 15.760217349728919
+Commit: 0.007025024002359714
```

```
Insercion de las frases:
Mean: 7.110907599189886e-05
Median: 5.852549975315924e-05
Standard deviation: 4.448110917449437e-05
Min: 4.268200018486823e-05
Max: 0.0006301590001385193
Total: 0.07110907599189886
+Commit: 0.0026585620003061194

Insercion de los embeddings:
Mean: 0.0008757498020045205
Median: 0.0008362915002635418
Standard deviation: 0.0001736126120642357
Min: 0.0006689429997095431
Max: 0.0022360399998433422
Total: 0.8757498020045205
+Commit: 0.001837351000176568
```

### Search

`3-postgres-search-1.py` - Se calcula la distancia en la aplicación
```
Mean: 3.0800568107981237
Median: 3.033931724501599
Standard deviation: 0.09391454098578557
Min: 3.005648909995216
Max: 3.2945583580003586
Total: 30.800568107981235
```

`3-postgres-search-2.py` - Se calcula la distancia en la base de datos mediante procedimientos almacenados
```
Mean: 1.1980004242992437
Median: 1.1968830794976384
Standard deviation: 0.0027701105036759288
Min: 1.196045400996809
Max: 1.2049168320008903
Total: 11.980004242992436
```

## Chroma

### Upload

`4-chroma-upload-1.py` - Se insertan de uno en uno
```
Mean: 0.0141900247771031
Median: 0.014240314998460235
Standard deviation: 0.005950451766164331
Min: 0.0038961320024100132
Max: 0.11468897099985043
Total: 141.900247771031
```

`4-chroma-upload-2.py` - Se insertan en batches de 5000
```
Mean: 2.121569818998978
Median: 2.121569818998978
Standard deviation: 0.18392871128253194
Min: 1.991512579996197
Max: 2.251627058001759
Total: 4.243139637997956
```

### Search

`5-chroma-search-1.py` - Búsqueda en Chroma
```
Mean: 0.012714183200296247
Median: 0.004595461497956421
Standard deviation: 0.02143564114608802
Min: 0.0033716470061335713
Max: 0.07204790900141234
Total: 0.12714183200296247
```

## pgvector

### Upload

`6-pgvector-upload-1.py` - Inserción en una única transacción con tipo de datos vector (de pgVector)
```
Mean: 0.0016513850076997187
Median: 0.0015649560009478591
Standard deviation: 0.0008999746693259508
Min: 0.0014184539977577515
Max: 0.0741301879970706
Total: 16.513850076997187
+Commit: 0.0004285429968149401
```

### Search

`7-pgvector-search-1.py` - Búsqueda con los procedimientos almacenados de distancia proporcionados pgVector, sin índices
```
Mean: 0.020380806498724268
Median: 0.019206710498110624
Standard deviation: 0.003765175714838944
Min: 0.018224845996883232
Max: 0.030947442995966412
Total: 0.2038080649872427
```

`7-pgvector-search-2.py` - Búsqueda con los procedimientos almacenados de distancia proporcionados pgVector, con índices (hnsw, los mismos que en chroma)
```
Mean: 0.003877481500967406
Median: 0.003680055004224414
Standard deviation: 0.0011371715484366687
Min: 0.0026671789964893833
Max: 0.006184751000546385
Total: 0.03877481500967406
```
