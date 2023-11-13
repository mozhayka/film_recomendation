# Подбор фильма для совместного просмотра
Проект 56 в рамках хакатона по рекомендации фильмов

## Архитектура
Есть приблизительные интерфейсы, их можно улучшать, если есть идеи как

### src/
#### algorithms
Реализация BFS для двух изначально заданных фильмов с целью найти средний между ними. Нужно найти такой фильм, чтобы был наиболее интересен обоим зрителям, поэтому минимизируем расстояние от него до двух изначальных

#### db
Запросы на получения информации с сайтов могут выполняться долго, поэтому после одного запроса сохраняем фильм и его "соседей" к себе в базу данных, чтобы при следующих запросах этого же фильма можно было подгружать эту информацию из базы.

#### main_body
Тут хранятся основные структуры для работы

#### site_requests
Выполняем запросы к сайтам с фильмами. Реализуем сами запросы на Go, затем передаем json-ы и парсим в Python

#### telegram_bot
Принимаем из чата в телеграме 2 фильма и обратно возвращаем результат
