from datetime import datetime
from typing import List

from dataclasses import dataclass


# Чтобы различать фильмы, можем хранить названия и url (или несколько url для нескольких сайтов)
# Возможно в будущем добавление актерского состава например
@dataclass
class FilmId:
    name: str
    url: str


# Это вершины дерева, по которому будем ходить
@dataclass
class Vertex:
    val: FilmId
    source: str
    similar: List[FilmId]


# То, что возвращаем пользователю
@dataclass
class Answer:
    recommended_films: List[FilmId]
