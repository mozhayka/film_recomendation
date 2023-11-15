import asyncio
from typing import List

from src.alogrithms.tree import Tree, intersect_trees
from src.structures import FilmId, Answer, VertexDto
from test.test_data import vertexes


async def get_neighbors(f: FilmId) -> List[FilmId]:
    vertex = vertexes[f]
    return vertex.similar


async def next_level(t: Tree):
    coroutines = [get_neighbors(film) for film in t.current_level]
    t.current_level.clear()

    for future in asyncio.as_completed(coroutines):
        result = await future
        for film in result:
            if film not in t.vertexes:
                t.vertexes.add(film)
                t.current_level.append(film)


# По двум фильмам запускает БФС, возвращает некоторый список подходящих фильмов
async def do_search_test(f1: FilmId, f2: FilmId) -> Answer:
    t1 = Tree(current_level=[f1], vertexes={f1})
    t2 = Tree(current_level=[f2], vertexes={f2})

    intersect = intersect_trees(t1, t2)
    while intersect is None:
        await next_level(t1)
        await next_level(t2)
        intersect = intersect_trees(t1, t2)
    ans = Answer(recommended_films=intersect)
    return ans