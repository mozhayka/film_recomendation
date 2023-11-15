from src.db.interfaces import save_to_base, get_from_base
from src.structures import FilmId, Vertex
import requests


def json_to_vertex(json) -> Vertex:
    pass


# Делает GET запросы к парсеру на Go, парсит полученные json-ы и возвращает Vertex
def get_request(film: FilmId) -> Vertex:
    if film.url is None:
        params = {{"by": "title", "query": film.name}}
        response = requests.get('http://127.0.0.1:8080/ivi/films', params)
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
