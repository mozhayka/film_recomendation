import json
from datetime import datetime, timedelta

import psycopg2
from psycopg2 import sql

from src.structures import VertexDto, FilmId, VertexEntity

def save_to_base(a):
    pass 

def get_from_base(a):
    pass 

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
                source VARCHAR(255) NOT NULL,
                similar_list JSONB,
                updated_at timestamp NOT NULL,
                PRIMARY KEY ("url")
            );
        '''
        index_create_query = 'CREATE INDEX IF NOT EXISTS idx_name_source ON film (name, source);'
        cursor.execute(table_create_query)
        cursor.execute(index_create_query)
    conn.commit()


def save_to_database(v: VertexDto, conn):
    with conn.cursor() as cursor:
        insert_query = sql.SQL('''
            INSERT INTO film (name, url, source, similar_list, updated_at)
            VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
            ON CONFLICT (url) DO UPDATE
            SET similar_list = EXCLUDED.similar_list, updated_at = CURRENT_TIMESTAMP;
        ''')

        similar_list_json = json.dumps(v.similar, default=film_id_serializer) if v.similar else None

        cursor.execute(insert_query, (v.val.name, v.val.url, v.source, similar_list_json,))
    conn.commit()


def get_from_database(film_id: FilmId, conn):
    with conn.cursor() as cursor:
        select_query = sql.SQL('''
            SELECT name, url, source, similar_list, updated_at
            FROM film
            WHERE url = %s;
           ''')
        cursor.execute(select_query, (film_id.url,))
        result = cursor.fetchone()

    if result:
        (name, url, source, similar_list, updated_at) = result
        if not name:
            return None
        if datetime.utcnow() - updated_at > timedelta(weeks=1):
            return None
        similar_list = similar_list if similar_list else []
        similar_list = [FilmId(name=v['name'], url=v['url']) for v in similar_list]
        return VertexEntity(FilmId(name=name, url=url), source=source, updated_at=updated_at, similar=similar_list)
    else:
        return None


def get_from_database_forced(film_id: FilmId, conn):
    with conn.cursor() as cursor:
        select_query = sql.SQL('''
            SELECT name, url, source, similar_list, updated_at
            FROM film
            WHERE url = %s;
           ''')
        cursor.execute(select_query, (film_id.url,))
        result = cursor.fetchone()

    if result:
        (name, url, source, similar_list, updated_at) = result
        similar_list = similar_list if similar_list else []
        similar_list = [FilmId(name=v['name'], url=v['url']) for v in similar_list]
        return VertexEntity(FilmId(name=name, url=url), source=source, updated_at=updated_at, similar=similar_list)
    else:
        return None


def film_id_serializer(obj):
    if isinstance(obj, FilmId):
        return {'name': obj.name, 'url': obj.url}
    raise TypeError("Type not serializable")
