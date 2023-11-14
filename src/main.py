from src.alogrithms.algo import do_search
from src.telegram_bot.interfaces import read_input, print_answer


# Скорее всего центр программы должен находиться внутри бота, оттуда соответственно идут вызовы do_search()
# так что эта часть будет переписана
def main():
    [film1, film2] = read_input()
    print_answer(do_search(film1, film2))
