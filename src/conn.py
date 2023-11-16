from src.db.film_dao import connect_to_database

conn = connect_to_database("film_recommendation", "root", "pwd123", "postgres", "5432")