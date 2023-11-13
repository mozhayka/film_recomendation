from typing import Optional

from src.Python.main_body.structures import Vertex, FilmId


# Сохраняет вершину дерева в базу. Если уже есть, то перезаписывает
def save_to_base(v: Vertex) -> None:
    pass

# Возвращает по названию фильма (или url) вершину (ее саму и соседей). Если вершины нет в базе, возвращает null
def get_from_base(id: FilmId) -> Optional[Vertex]:
    pass