from typing import List

from dataclasses import dataclass


# Чтобы различать фильмы, можем хранить названия и url (или несколько url для нескольких сайтов)
# Возможно в будущем добавление актерского состава например
@dataclass
class FilmId:
    name: str
    url: str

    def __hash__(self):
        return hash(self.url)

    def __eq__(self, other):
        return self.url == other.url


# Это вершины дерева, по которому будем ходить
@dataclass
class Vertex:
    val: FilmId
    similar: List[FilmId]


# То, что возвращаем пользователю
@dataclass
class Answer:
    recommended_films: List[FilmId]
