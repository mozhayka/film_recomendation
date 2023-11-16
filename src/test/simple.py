import asyncio

from src.algorithms.algo import do_search
from src.structures import FilmId

f1 = FilmId(name="Брат", url="https://www.ivi.tv/watch/33531")
f2 = FilmId(name="57 секунд", url="https://www.ivi.tv/watch/515974")

async def test1():
    ans = await do_search(f1, f2)
    print(ans.recommended_films)

if __name__ == "__main__":
    asyncio.run(test1())
    # test1()