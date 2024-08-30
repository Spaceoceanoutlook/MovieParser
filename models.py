from sqlalchemy.orm import declarative_base, mapped_column, relationship
from sqlalchemy.orm import Mapped
from sqlalchemy import Integer, String, ForeignKey, create_engine
from typing import List

# Создание движка
engine = create_engine('sqlite:///my_films.db')

# Определение базового класса
Base = declarative_base()


class FilmGenre(Base):
    __tablename__ = 'film_genre'

    film_id: Mapped[int] = mapped_column(ForeignKey('films.id'), primary_key=True)
    genre_id: Mapped[int] = mapped_column(ForeignKey('genres.id'), primary_key=True)


class FilmCountry(Base):
    __tablename__ = 'film_country'

    film_id: Mapped[int] = mapped_column(ForeignKey('films.id'), primary_key=True)
    country_id: Mapped[int] = mapped_column(ForeignKey('countries.id'), primary_key=True)


class Film(Base):
    __tablename__ = 'films'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, unique=True)
    year: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(String)
    rating: Mapped[int] = mapped_column(Integer)
    img: Mapped[str] = mapped_column(String)
    # Связи
    genres: Mapped[List["Genre"]] = relationship("Genre", secondary="film_genre", back_populates="films")
    countries: Mapped[List["Country"]] = relationship("Country", secondary="film_country", back_populates="films")


class Genre(Base):
    __tablename__ = 'genres'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    # Связь с фильмами
    films: Mapped[List["Film"]] = relationship("Film", secondary="film_genre", back_populates="genres")


class Country(Base):
    __tablename__ = 'countries'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    # Связь с фильмами
    films: Mapped[List["Film"]] = relationship("Film", secondary="film_country", back_populates="countries")


if __name__ == '__main__':
    # Создание таблиц
    Base.metadata.create_all(engine)
