from pydantic import BaseModel


class FilmResponse(BaseModel):
    title: str
    year: int
    countries: list[str]
    genres: list[str]
    description: str
    rating: float
    img: str


class UserCreate(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True
