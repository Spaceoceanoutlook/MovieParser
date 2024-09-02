from fastapi import FastAPI, Request
import uvicorn
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from views import main, get_films_from_db

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/")
async def submit_link(request: Request):
    form_data = await request.form()  # Получаем данные формы
    url = form_data.get('text')  # Извлекаем значение по ключу 'text'
    main(url)  # Передаем ссылку в парсинг
    #  status_code=303 (See Other), который указывает браузеру выполнить GET-запрос
    return RedirectResponse(url="/films", status_code=303)  # Перенаправляем на страницу films


@app.get("/films", response_class=HTMLResponse)
async def films(request: Request):
    all_films = get_films_from_db()  # Получаем фильмы из базы данных
    context = {"request": request, "films": all_films}
    return templates.TemplateResponse("films.html", context=context)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
