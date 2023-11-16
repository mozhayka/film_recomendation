from src.conn import conn
from src.db.film_dao import save_to_base, get_from_base
from src.structures import FilmId, VertexDto
from typing import List

import requests
from src.db.film_dao import save_to_database, get_from_database
from src.structures import FilmId, VertexDto


def json_to_vertex(json, mode: str) -> VertexDto:
    movie_data = json['movie']
    film_id = FilmId(name=movie_data['title'], url=movie_data['link'])
    recommended_movie_data = json['recommended_movies']
    recommended_movies = [FilmId(name=item['title'], url=item['link']) for item in recommended_movie_data]

    return VertexDto(val=film_id, source=mode, similar=recommended_movies)


# Делает GET запросы к парсеру на Go, парсит полученные json-ы и возвращает Vertex
def get_request(film: FilmId, mode: str='ivi') -> VertexDto:
    vertex = get_from_database(film, conn)
    if vertex is None:
        params = {"by": "link", "query": film.url}
        response = requests.get(f'http://parser:8080/{mode}/films', json=params)
        if response.status_code != 200:
            print(response.json())
            # return VertexDto  # TODO: return error form json response

        json_response = response.json()
        vertex = json_to_vertex(json_response, mode)
        save_to_database(vertex, conn)
        return vertex
    # else:
    #     vertex.similar = [FilmId(name=v['name'], url=v['url']) for v in vertex.similar]

    return vertex


def suggest(query: str, mode: str) -> List[FilmId]:
    params = {"prefix": query}
    response = requests.get(f'http://parser:8080/{mode}/predicts', json=params)
    json_response = response.json()
    vertex = json_to_vertex(json_response, mode)
    # save_to_base(vertex)
    return vertex.similar
