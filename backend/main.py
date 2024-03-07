from fastapi import FastAPI
from core.config import settings
from db.session import engine
from db.base_class import Base
import requests


def create_tables():
    Base.metadata.create_all(bind=engine)


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    create_tables()
    return app


app = start_application()


@app.get("/")
def home():
    return {"msg": "Hello FastAPI🚀"}


@app.get("/movie/{movie_id}")
async def get_movie_detail(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {settings.TMDB_BEARER}",
    }

    response = requests.get(url, headers=headers)

    return response.json()


@app.get("/tvShow/{show_id}")
async def get_show_detail(show_id):
    url = f"https://api.themoviedb.org/3/tv/{show_id}?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {settings.TMDB_BEARER}",
    }

    response = requests.get(url, headers=headers)

    return response.json()
