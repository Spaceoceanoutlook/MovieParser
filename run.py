from fastapi import FastAPI, Request
import uvicorn
from fastapi.responses import FileResponse
from main import main

app = FastAPI()


@app.get("/")
async def index():
    return FileResponse("templates/index.html")


@app.post("/submit")
async def submit_link(request: Request):
    form_data = await request.form()  # Получаем данные формы
    url = form_data.get('text')  # Извлекаем значение по ключу 'text'
    main(url)    # Передаем ссылку в парсинг
    return FileResponse("templates/index.html")


if __name__ == "__main__":
    uvicorn.run("run:app", reload=True)
