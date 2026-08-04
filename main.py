from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
import pydantic
import secrets

app = FastAPI(title="URL Shortener")

# Наша "база данных" в оперативной памяти
db = {}

# Схема валидации входящих данных (аналог DTO или Request Validation в PHP)
class URLRequest(pydantic.BaseModel):
    url: pydantic.HttpUrl

@app.post("/shorten")
def shorten_url(request: URLRequest):
    # Генерируем случайный хэш из 6 символов
    short_id = secrets.token_urlsafe(4)[:6]
    
    # Сохраняем в словарь (в Python приведение типов строк автоматическое)
    db[short_id] = str(request.url)
    
    return {"short_url": f"http://localhost:8000/{short_id}"}

@app.get("/{short_id}")
def redirect_to_url(short_id: str):
    # Ищем ссылку в нашей "базе"
    long_url = db.get(short_id)
    
    if not long_url:
        raise HTTPException(status_code=404, detail="Ссылка не найдена")
        
    # Делаем 307 редирект (временный)
    return RedirectResponse(url=long_url, status_code=307)
