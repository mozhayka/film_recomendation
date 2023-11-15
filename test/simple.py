from test.algo_test import do_search_test
from test.test_data import f1, f2


async def test1():
    ans = await do_search_test(f1, f2)
    print(ans.recommended_films)
