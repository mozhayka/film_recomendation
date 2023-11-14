import json
import psycopg2
from psycopg2 import sql

from src.structures import Vertex, FilmId


def connect_to_database(dbname, user, password, host, port):
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    return conn


def create_table_if_not_exists(conn):
    with conn.cursor() as cursor:
        table_create_query = '''
            CREATE TABLE IF NOT EXISTS film (
                name VARCHAR(255) NOT NULL,
                url VARCHAR(255) NOT NULL,
                similar_list JSONB,
                PRIMARY KEY (name, url)
            );
        '''
        cursor.execute(table_create_query)
    conn.commit()


def save_to_database(v: Vertex, conn):
    with conn.cursor() as cursor:
        insert_query = sql.SQL('''
            INSERT INTO film (name, url, similar_list)
            VALUES (%s, %s, %s)
            ON CONFLICT (name, url) DO UPDATE
            SET similar_list = EXCLUDED.similar_list;
        ''')
        film_id_tuple = (v.val.name, v.val.url)
        similar_list_json = json.dumps(v.similar, default=film_id_serializer) if v.similar else None
        cursor.execute(insert_query, film_id_tuple + (similar_list_json,))
    conn.commit()


def get_from_database(filmId: FilmId, conn):
    with conn.cursor() as cursor:
        select_query = sql.SQL('''
            SELECT name, url, similar_list
            FROM film
            WHERE name = %s AND url = %s;
           ''')
        cursor.execute(select_query, (filmId.name, filmId.url))
        result = cursor.fetchone()

    if result:
        similar_list = result[2] if result[2] else []
        return Vertex(FilmId(name=result[0], url=result[1]), similar=similar_list)
    else:
        return None


def film_id_serializer(obj):
    if isinstance(obj, FilmId):
        return {'name': obj.name, 'url': obj.url}
    raise TypeError("Type not serializable")
