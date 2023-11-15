from datetime import datetime, timedelta

from src.conn import conn
from typing import List

import requests
from src.db.film_dao import save_to_database, get_from_database
from src.structures import FilmId, VertexDto

MAX_REQUEST_TIMEOUT = 1200
DEFAULT_REQUEST_TIMEOUT = 20


def json_to_vertex(json, mode: str) -> VertexDto:
    movie_data = json['movie']
    film_id = FilmId(name=movie_data['title'], url=movie_data['link'])
    recommended_movie_data = json['recommended_movies']
    recommended_movies = [FilmId(name=item['title'], url=item['link']) for item in recommended_movie_data]

    return VertexDto(val=film_id, source=mode, similar=recommended_movies)


def get_request(film_id: FilmId, mode: str = 'ivi') -> VertexDto:
    vertex = get_from_database_with_timeout(film_id, mode)
    if vertex is not None:
        return vertex

    return get_recommended_films(film_id, mode)


def get_from_database_with_timeout(film_id: FilmId, mode: str):
    vertex = get_from_database(film_id, conn)

    if vertex is not None and vertex.updated_at:
        time_difference = datetime.utcnow() - vertex.updated_at
        if time_difference > timedelta(weeks=1):
            try:
                vertex = get_recommended_films(film_id, mode, timeout=DEFAULT_REQUEST_TIMEOUT)
            except requests.Timeout:
                return vertex

    return vertex


def get_recommended_films(film_id: FilmId, mode: str = 'ivi', timeout=MAX_REQUEST_TIMEOUT) -> VertexDto:
    params = {"by": "link", "query": film_id.url}
    response = requests.get(f'http://parser:8080/{mode}/films', json=params, timeout=timeout)
    response.raise_for_status()  # throw exception if status not 200

    json_response = response.json()
    vertex = json_to_vertex(json_response, mode)
    save_to_database(vertex, conn)
    return vertex


def suggest(query: str, mode: str) -> List[FilmId]:
    params = {"prefix": query}
    response = requests.get(f'http://parser:8080/{mode}/predicts', json=params)
    json_response = response.json()
    vertex = json_to_vertex(json_response, mode)
    # save_to_base(vertex)
    return vertex.similar
