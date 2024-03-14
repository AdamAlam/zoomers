import datetime
from typing import Optional

import requests
from core.config import settings
from db.base_class import Base
from db.models import Review
from db.schemas import ReviewCreate, ReviewResponse
from db.session import SessionLocal, engine
from fastapi import Depends, FastAPI, HTTPException, status
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


# Get all reviews
@app.get("/allReviews/")
async def get_all_reviews(db: Session = Depends(get_db)):
    db_response = db.query(Review).all()
    return db_response


# New Review
@app.post(
    "/reviews/", response_model=ReviewResponse
)  # Ensure ReviewResponse matches your desired output structure
async def create_review(review_data: ReviewCreate, db: Session = Depends(get_db)):
    existing_review = (
        db.query(Review)
        .filter(Review.User == review_data.User, Review.MediaId == review_data.MediaId)
        .first()
    )

    if existing_review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A review by user {review_data.User} for media {review_data.MediaId} already exists.",
        )

    new_review = Review(
        User=review_data.User,
        stars=review_data.stars,
        ReviewText=review_data.ReviewText,
        MediaId=review_data.MediaId,
        Date=datetime.datetime.now(datetime.UTC),
    )
    db.add(new_review)
    try:
        db.commit()
        db.refresh(new_review)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    return new_review


# TODO: Routes to Create
# - Search Movies
# - Search TV Shows
# - Follow User
# - Unfollow User
# - User Created
# - User Updated
# - Get Reviews of Following
# - Get Reviews of User
# - Get Reviews of Movie/TV Show
