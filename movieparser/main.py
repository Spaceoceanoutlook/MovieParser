from fastapi import FastAPI, Request
import uvicorn
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from views import main, get_films_from_db, get_one_film_from_db, get_films_by_genre, get_films_by_country, register_user
from schemas import UserCreate

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("add_film.html", {"request": request})


@app.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register", response_class=HTMLResponse)
async def get_data_register(request: Request):
    form_data = await request.form()  # Получаем данные формы
    username = form_data.get('username')
    password = form_data.get('password')
    user = UserCreate(username=username, password=password)
    user = register_user(user)
    response = RedirectResponse(url="/films", status_code=303)
    response.set_cookie(key="user_id", value=str(user.id))  # Записываем user_id в куку
    response.set_cookie(key="username", value=str(user.username))  # Записываем username в куку
    return response
    # return RedirectResponse(url="/films", status_code=303)


@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/")
async def submit_link(request: Request):
    form_data = await request.form()  # Получаем данные формы
    link = form_data.get('link')  # Извлекаем значение из формы где name = link
    main(link)  # Передаем ссылку в парсинг
    #  status_code=303 (See Other), который указывает браузеру выполнить GET-запрос
    return RedirectResponse(url="/films", status_code=303)  # Перенаправляем на страницу films


@app.get("/films", response_class=HTMLResponse)
async def films(request: Request):
    user_id = request.cookies.get("user_id")  # Получаем из куки
    username = request.cookies.get("username")  # Получаем из куки
    all_films = get_films_from_db()  # Получаем фильмы из базы данных
    context = {"request": request, "films": all_films, 'username': username}
    return templates.TemplateResponse("films.html", context=context)


@app.get("/films/{film_id}", response_class=HTMLResponse)
def get_film(film_id, request: Request):
    film = get_one_film_from_db(film_id)
    context = {"request": request, "film": film}
    return templates.TemplateResponse("films.html", context=context)


@app.get("/films/genre/{genre_name}", response_class=HTMLResponse)
def get_genre(genre_name, request: Request):
    all_films = get_films_by_genre(genre_name)
    context = {"request": request, "films": all_films}
    return templates.TemplateResponse("films.html", context=context)


@app.get("/films/country/{country_name}", response_class=HTMLResponse)
def get_genre(country_name, request: Request):
    all_films = get_films_by_country(country_name)
    context = {"request": request, "films": all_films}
    return templates.TemplateResponse("films.html", context=context)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
