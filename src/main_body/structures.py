from typing import List

from dataclasses import dataclass

@dataclass
class FilmId:
    name: str
    url: str

@dataclass
class Vertex:
    val: FilmId
    similar: List<FilmId>

@dataclass
class Answer:
    recommended_films: List<FilmId>