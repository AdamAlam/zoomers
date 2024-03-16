import datetime
from typing import Optional

import bcrypt
import requests
from core.config import settings
from db.base_class import Base
from db.models import Review, User
from db.schemas import ReviewByMediaResponse, ReviewCreate, ReviewResponse, UserCreate
from db.session import SessionLocal, engine
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from util.generateJWT import generate_jwt


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
@app.post("/reviews/", response_model=ReviewResponse)
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


# TODO: Maybe we should return name instead of display name?
@app.get("/reviews/{media_id}", response_model=list[ReviewByMediaResponse])
async def get_reviews_by_media_id(media_id: int, db: Session = Depends(get_db)):
    db_response = (
        db.query(
            Review.id,
            Review.stars,
            Review.ReviewText,
            Review.Date,
            Review.MediaId,
            User.DisplayName,
        )
        .join(User, Review.User == User.id)
        .filter(Review.MediaId == media_id)
        .all()
    )

    result = [
        ReviewByMediaResponse(
            id=review.id,
            stars=review.stars,
            ReviewText=review.ReviewText,
            Date=review.Date,
            MediaId=review.MediaId,
            DisplayName=review.DisplayName,
        )
        for review in db_response
    ]

    return result


@app.post("/signup/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.Email == user.Email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email {user.Email} already exists.",
        )

    hashed_pass = bcrypt.hashpw(user.Password.encode("utf-8"), bcrypt.gensalt()).decode(
        "utf-8"
    )
    new_user = User(
        Email=user.Email,
        Username=user.Username,
        PasswordHash=hashed_pass,
        DisplayName=user.DisplayName,
        Bio=user.Bio,
        ProfilePictureUrl=user.ProfilePictureUrl,
        IsPrivate=user.IsPrivate,
        FirstName=user.FirstName,
        LastName=user.LastName,
    )

    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    return new_user


# TODO: We should pass our params as headers, not as query params
@app.post("/login/")
def login_user(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.Email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email {email} not found.",
        )

    if not bcrypt.checkpw(password.encode("utf-8"), bytes(user.PasswordHash, "utf-8")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password."
        )

    # TODO: Generate JWT token and return it
    JWT = generate_jwt(user.id)
    return {"jwt": JWT}
