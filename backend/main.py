from typing import Optional

import requests
from db.models import Review
from core.config import settings
from db.base_class import Base
from db.session import engine
from db.session import SessionLocal
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session


def create_tables():
    Base.metadata.create_all(bind=engine)


origins = ["http://localhost:3000"]


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    create_tables()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

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


@app.get("/movies/popular/")
async def get_popular_movies(page: Optional[str] = 1):
    url = f"https://api.themoviedb.org/3/movie/popular?language=en-US&page={page}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {settings.TMDB_BEARER}",
    }

    response = requests.get(url, headers=headers)

    return response.json()


@app.get("/tvShows/popular/")
async def get_popular_shows(page: Optional[str] = 1):
    url = f"https://api.themoviedb.org/3/tv/popular?language=en-US&page={page}"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {settings.TMDB_BEARER}",
    }

    response = requests.get(url, headers=headers)

    return response.json()


@app.get("/allReviews/")
async def get_all_reviews(db: Session = Depends(get_db)):
    db_response = db.query(Review).all()
    return db_response


# TODO: Routes to Create
# - Search Movies
# - Search TV Shows
# - Follow User
# - Unfollow User
# - User Created
# - User Updated
# - New Review
# - Get Reviews of Following
# - Get Reviews of User
# - Get Reviews of Movie/TV Show
