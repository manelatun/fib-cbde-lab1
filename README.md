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
Mean: 0.0001018159439999522
Median: 0.00010870300000931366
Standard deviation: 4.2727687014249586e-05
Min: 5.360699998391283e-05
Max: 0.0005635619999964092
Total: 0.1018159439999522
+Commit: 0.0054194670000242695

Insercion de los embeddings:
Mean: 0.0005910180680001816
Median: 0.0005458644999976059
Standard deviation: 0.0002511934730200177
Min: 0.00047812299999350216
Max: 0.005048977999990711
Total: 0.5910180680001815
+Commit: 0.028641378000003215
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

Mean: 0.10509927220000463
Median: 0.09851612700003898
Standard deviation: 0.01775927871804627
Min: 0.09478738500001782
Max: 0.15333371599990642
Total: 1.0509927220000463
```

`3-postgres-search-2.py` - Se calcula la distancia en la base de datos mediante procedimientos almacenados
```
Mean: 1.1980004242992437
Median: 1.1968830794976384
Standard deviation: 0.0027701105036759288
Min: 1.196045400996809
Max: 1.2049168320008903
Total: 11.980004242992436

Mean: 0.03992935180003769
Median: 0.039830442500033314
Standard deviation: 0.0027668496936670184
Min: 0.03720662000023367
Max: 0.046756200000345416
Total: 0.39929351800037693
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

Tiempo de insercion de las frases:
Mean: 0.20494509612700312
Median: 0.1926857485000255
Standard deviation: 0.31989421894848147
Min: 0.1411800559999392
Max: 10.285207652000281
Total: 204.94509612700313

Tiempo de insercion de los embeddings:
Mean: 0.017874681147003683
Median: 0.017276217000244287
Standard deviation: 0.0031493461380636407
Min: 0.012882124000043405
Max: 0.050989644000310363
Total: 17.874681147003685
```

`4-chroma-upload-2.py` - Se insertan en batches de 5000
```
Mean: 2.121569818998978
Median: 2.121569818998978
Standard deviation: 0.18392871128253194
Min: 1.991512579996197
Max: 2.251627058001759
Total: 4.243139637997956

Tiempo de insercion de las frases:
Mean: 19.374892774000045
Median: 19.374892774000045
Standard deviation: 1.3641751906000341
Min: 18.41027524600031
Max: 20.33951030199978
Total: 38.74978554800009
Batch size: 500

Tiempo de insercion de los embeddings:
Mean: 0.22003472799974588
Median: 0.22003472799974588
Standard deviation: 0.04105465224278975
Min: 0.19100470499961375
Max: 0.24906475099987802
Total: 0.44006945599949177
Batch size: 500
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

Mean: 0.0031504120001955016
Median: 0.002140374000191514
Standard deviation: 0.0030999502320698084
Min: 0.0015459720007129363
Max: 0.011885041999448731
Total: 0.031504120001955016
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

Tiempo de insercion de las frases:
Mean: 9.5358962013961e-05
Median: 0.0001058450006894418
Standard deviation: 5.562216419912558e-05
Min: 4.585900023812428e-05
Max: 0.0009606759995222092
Total: 0.09535896201396099
+Commit: 0.004390870999486651

Tiempo de insercion de los embeddings:
Mean: 0.0007050812790112104
Median: 0.0006104570002207765
Standard deviation: 0.0002913277742679381
Min: 0.00045532300009654136
Max: 0.003360691000125371
Total: 0.7050812790112104
+Commit: 0.0023185309992186376
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

Mean: 0.001697654299914575
Median: 0.0011233764998905826
Standard deviation: 0.0014862508653669293
Min: 0.001012746999549563
Max: 0.0057820860001811525
Total: 0.01697654299914575
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
