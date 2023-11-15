from src.algorithms.algo import do_search
from src.structures import FilmId


f1 = FilmId(name="Брат 2", url="")
f2 = FilmId(name="57 секунд", url="")


async def test1():
    ans = await do_search(f1, f2)
    print(ans.recommended_films)
