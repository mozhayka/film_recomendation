import asyncio
from typing import List

from src.algorithms.tree import Tree, intersect_trees
from src.parser_requests.interfaces import get_request
from src.structures import FilmId, Answer


async def get_neighbors(f: FilmId, mode) -> List[FilmId]:
    vertex = await get_request(f, mode)
    return vertex.similar


async def next_level(t: Tree, mode):
    coroutines = [get_neighbors(film, mode) for film in t.current_level]
    t.current_level.clear()
    #
    # for future in asyncio.as_completed(coroutines):

    results = await asyncio.gather(*coroutines)
    for result in results:
        for film in result:
            if film not in t.vertexes:
                t.vertexes.add(film)
                t.current_level.append(film)


# По двум фильмам запускает БФС, возвращает некоторый список подходящих фильмов
async def do_search(f1: FilmId, f2: FilmId, mode='ivi') -> Answer:
    t1 = Tree(current_level=[f1], vertexes={f1})
    t2 = Tree(current_level=[f2], vertexes={f2})

    intersect = intersect_trees(t1, t2)
    while intersect is None:
        await next_level(t1, mode)
        await next_level(t2, mode)
        intersect = intersect_trees(t1, t2)
    ans = Answer(recommended_films=intersect)
    return ans
