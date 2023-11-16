import aiohttp as aiohttp

from src.conn import conn
from typing import List

import requests
from src.db.film_dao import save_to_database, get_from_database, get_from_database_forced
from src.structures import FilmId, VertexDto


mods = ['ivi']


def json_to_vertex(json, mode: str) -> VertexDto:
    movie_data = json['movie']
    film_id = FilmId(name=movie_data['title'], url=movie_data['link'])
    recommended_movie_data = json['recommended_movies']
    recommended_movies = [FilmId(name=item['title'], url=item['link']) for item in recommended_movie_data]

    return VertexDto(val=film_id, source=mode, similar=recommended_movies)


# Делает GET запросы к парсеру на Go, парсит полученные json-ы и возвращает Vertex
async def get_request(film: FilmId, mode: str) -> VertexDto:
    vertex = get_from_database(film, conn)
    if vertex is None:
        params = {"by": "link", "query": film.url}
        async with aiohttp.ClientSession() as session:
            async with session.get(f'http://parser:8080/{mode}/films', json=params) as response:
                if response.status != 200:
                    return get_from_database_forced(film, conn)

                json_response = await response.json()
                vertex = json_to_vertex(json_response, mode)
                save_to_database(vertex, conn)
                return vertex

    return vertex


def suggest(query: str, mode: str) -> List[FilmId]:
    params = {"prefix": query}
    response = requests.get(f'http://parser:8080/{mode}/predicts', json=params)
    json_response = response.json()
    vertex = json_to_vertex(json_response, mode)
    return vertex.similar

