import logging
from service import get_information_about_the_movie
from sqlalchemy.orm import sessionmaker, joinedload
from movieparser.models import engine, Film, Genre, Country, User
from schemas import FilmResponse, UserCreate
from pydantic import ValidationError
import bcrypt
from fastapi import HTTPException

# Настройка логирования
logger = logging.getLogger(__name__)
FORMAT = '%(asctime)s:%(name)s:%(levelname)s:%(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

# Создание сессии
Session = sessionmaker(bind=engine)


def hash_password(password: str) -> str:
    # Генерация соли и хэширование пароля
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Проверка соответствия пароля и хэша
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def add_genres_to_film(session, film, genres):
    genres_to_add = []
    for genre_name in genres:
        genre_name = genre_name.strip().capitalize()
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
        if country_name not in ['США', 'СССР']:
            country_name = country_name.strip().capitalize()
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
        try:
            # Создаем экземпляр FilmResponse для валидации данных
            FilmResponse(**data)  # Если данные валидны, ничего не произойдет
        except ValidationError as e:
            # Обрабатываем ошибки валидации, если они есть
            print("Ошибка валидации:", e.json())
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


def get_films_from_db():
    with Session() as session:
        # Подгружаем сразу связанные таблицы
        films = (session.query(Film)
                 .options(joinedload(Film.countries))
                 .options(joinedload(Film.genres))
                 .all())
        films.reverse()
    return films


def get_one_film_from_db(film_id: int):
    with Session() as session:
        film = (session.query(Film)
                .filter(Film.id == film_id)
                .options(joinedload(Film.countries))
                .options(joinedload(Film.genres))
                .first())
    return film


def get_films_by_genre(genre_name):
    with Session() as session:
        films = (session.query(Film)
                 .join(Film.genres)
                 .filter(Genre.name == genre_name)
                 .options(joinedload(Film.countries))
                 .options(joinedload(Film.genres))
                 .all())
    return films


def get_films_by_country(country_name):
    with Session() as session:
        films = (session.query(Film)
                 .join(Film.countries)
                 .filter(Country.name == country_name)
                 .options(joinedload(Film.countries))
                 .options(joinedload(Film.genres)).
                 all())
    return films


def register_user(user: UserCreate):
    with Session() as session:
        db_user = session.query(User).filter(User.username == user.username).first()
        if db_user:
            raise HTTPException(status_code=400, detail="Такой пользователь уже существует")
        # Хэшируем пароль перед сохранением
        hashed_password = hash_password(user.password)
        new_user = User(username=user.username, password=hashed_password)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
    return new_user
