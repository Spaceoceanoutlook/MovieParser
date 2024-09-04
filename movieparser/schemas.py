from pydantic import BaseModel


class FilmResponse(BaseModel):
    title: str
    year: int
    countries: list[str]
    genres: list[str]
    description: str
    rating: float
    img: str
