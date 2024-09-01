# MovieParser

Приложение позволяет ввести в браузере ссылку на фильм или сериал из 
https://www.kinopoisk.ru/ и информация автоматически добавится в базу данных.

http://127.0.0.1:8000/films - посмотреть базу данных фильмов

## **Запуск**

- git clone https://github.com/Spaceoceanoutlook/MovieParser.git
- poetry install (Установка библиотек)
- alembic upgrade head (Создание таблиц в БД)
- run.py