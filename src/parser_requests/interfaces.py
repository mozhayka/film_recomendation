from src.db.interfaces import save_to_base, get_from_base
from src.structures import FilmId, VertexDto
from typing import List
import requests


def json_to_vertex(json, mode: str) -> VertexDto:
    movie_data = json['movie']
    film_id = FilmId(name=movie_data['title'], url=movie_data['link'])

    recommended_movie_data = json['recommended_movies']
    recommended_movies = [FilmId(name=item['title'], url=item['link']) for item in recommended_movie_data]

    return VertexDto(val=film_id, source=mode, similar=recommended_movies)


# Делает GET запросы к парсеру на Go, парсит полученные json-ы и возвращает Vertex
def get_request(film: FilmId, mode: str) -> Vertex:
    if film.url is None:
        params = {{"by": "title", "query": film.name}}
        response = requests.get(f'http://127.0.0.1:8080/{mode}/films', params)
        json_response = response.json()
        vertex = json_to_vertex(json_response)
        save_to_base(vertex)
        return vertex

    vertex = get_from_base(film)
    if vertex is None:
        params = {{"by": "link", "query": film.url}}
        response = requests.get('http://127.0.0.1:8080/ivi/films', params)
        json_response = response.json()
        vertex = json_to_vertex(json_response)
        save_to_base(vertex)
        return vertex

    return vertex

def suggest(query: str, mode: str) -> List[FilmId]:
    pass
