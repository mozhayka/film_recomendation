import asyncio

from src.alogrithms.tree import Tree, intersect_trees
from src.structures import FilmId, Answer

async def next_level(t: Tree):
    pass

# По двум фильмам запускает БФС, возвращает некоторый список подходящих фильмов
async def do_search(f1: FilmId, f2: FilmId) -> Answer:
    t1 = Tree(current_level=asyncio.Queue(), vertexes=[f1])
    t2 = Tree(current_level=asyncio.Queue(), vertexes=[f2])
    await t1.current_level.put(f1)
    await t2.current_level.put(f2)

    intersect = intersect_trees(t1, t2)
    while intersect is None:
        next_level(t1)
        next_level(t2)
        intersect_trees(t1, t2)
    ans = Answer(recommended_films=intersect)
    return ans
