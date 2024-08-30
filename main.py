import logging
from service import get_information_about_the_movie
from sqlalchemy.orm import sessionmaker
from models import engine, Film, Genre, Country

# Настройка логирования
logger = logging.getLogger(__name__)
FORMAT = '%(asctime)s:%(name)s:%(levelname)s:%(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

# Создание сессии
Session = sessionmaker(bind=engine)


def add_genres_to_film(session, film, genres):
    genres_to_add = []
    for genre_name in genres:
        genre_name = genre_name.strip().title()
        genre = session.query(Genre).filter_by(name=genre_name).first()
        if genre is None:
            genre = Genre(name=genre_name)
            genres_to_add.append(genre)
        film.genres.append(genre)
    session.add_all(genres_to_add)
    logger.info('Жанры добавлены')


def add_countries_to_film(session, film, countries):
    countries_to_add = []
    for country_name in countries:
        country_name = country_name.strip().title()
        country = session.query(Country).filter_by(name=country_name).first()
        if country is None:
            country = Country(name=country_name)
            countries_to_add.append(country)
        film.countries.append(country)
    session.add_all(countries_to_add)
    logger.info('Страны добавлены')


def main(url_film):
    try:
        data = get_information_about_the_movie(url_film)
        logger.info('Информация о фильме успешно получена')
        with Session() as session:
            new_film = Film(
                title=data['title'],
                year=data['year'],
                description=data['description'],
                rating=data['rating'],
                img=data['img']
            )
            session.add(new_film)

            add_genres_to_film(session, new_film, data['genres'])
            add_countries_to_film(session, new_film, data['countries'])

            session.commit()
            logger.info('Успешно добавлен фильм: %s', new_film.title)
    except Exception as e:
        logger.error("Ошибка: %s", e)


if __name__ == "__main__":
    url = 'https://www.kinopoisk.ru/film/521689/'
    main(url)
