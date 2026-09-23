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

4. Ejecuta uno de los `2-postgres-upload-n.py`, todos hacen lo mismo pero con más o menos optimizaciones, la cabecera de cada fichero tiene más información. El mejor optimizado es el `2-posgres-upload-3.py`, que inserta todos los embeddings en una sola transaccion con un array de floats dee precisión simple.

5. Ejecuta uno de los `2-postgres-search-n.py`. El mejor optimizado es el `2-posgres-search-2.py`, que hace la búsqueda calculando las distancias con procedimientos almacenados en la base de datos.

## Chroma

6. 
