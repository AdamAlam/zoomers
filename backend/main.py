import datetime
from typing import Optional

import bcrypt
import requests
from core.config import settings
from db.base_class import Base
from db.models import Follow, Review, User
from db.schemas import (
    FollowCreate,
    ReviewByMediaResponse,
    ReviewCreate,
    ReviewResponse,
    UserCreate,
)
from db.session import SessionLocal, engine
from fastapi import Depends, FastAPI, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func
from sqlalchemy.orm import Session
from util.auth import generate_jwt, validate_jwt


def create_tables():
    """Create database tables based on SQLAlchemy models."""
    Base.metadata.create_all(bind=engine)


origins = ["http://localhost:3000"]


def get_db():
    """
    Dependency that provides a SQLAlchemy session for interacting with the database.
    It automatically handles session closing.

    Yields:
        Session: SQLAlchemy session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def start_application() -> FastAPI:
    """
    Initialize and configure the FastAPI application, including creating database tables
    and setting up CORS middleware.

    Returns:
        FastAPI: The configured FastAPI application.
    """
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
    """
    Root endpoint that returns a welcome message.

    Returns:
        dict: A welcome message.
    """
    return {"msg": "Hello FastAPI🚀"}


@app.get("/movie/{movie_id}")
async def get_movie_detail(movie_id: str):
    """
    Fetch and return the details of a movie from an external API using the movie ID.

    Args:
        movie_id (str): The ID of the movie to fetch details for.

    Returns:
        dict: The movie details as a JSON response.
    """
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {settings.TMDB_BEARER}",
    }

    response = requests.get(url, headers=headers, timeout=10)

    return response.json()


@app.get("/tvShow/{show_id}")
async def get_show_detail(show_id: str):
    """
    Fetch and return the details of a TV show from an external API using the show ID.

    Args:
        show_id (str): The ID of the TV show to fetch details for.

    Returns:
        dict: The TV show details as a JSON response.
    """
    url = f"https://api.themoviedb.org/3/tv/{show_id}?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {settings.TMDB_BEARER}",
    }

    response = requests.get(url, headers=headers, timeout=10)

    return response.json()


@app.get("/movies/popular/")
async def get_popular_movies(page: Optional[str] = 1):
    """
    Fetch and return a list of popular movies from an external API.

    Args:
        page (Optional[str], optional): The page number of movie listings to fetch. Defaults to 1.

    Returns:
        dict: The list of popular movies as a JSON response.
    """
    url = f"https://api.themoviedb.org/3/movie/popular?language=en-US&page={page}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {settings.TMDB_BEARER}",
    }

    response = requests.get(url, headers=headers, timeout=10)

    return response.json()


@app.get("/tvShows/popular/")
async def get_popular_shows(page: Optional[str] = 1):
    """
    Fetch and return a list of popular TV shows from an external API.

    Args:
        page (Optional[str], optional): The page number of TV show listings to fetch. Defaults to 1.

    Returns:
        dict: The list of popular TV shows as a JSON response.
    """
    url = f"https://api.themoviedb.org/3/tv/popular?language=en-US&page={page}"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {settings.TMDB_BEARER}",
    }

    response = requests.get(url, headers=headers, timeout=10)

    return response.json()


@app.get("/search/movies/{query}")
def search_movies(query: str, payload: dict = Depends(validate_jwt)):
    """
    Search for movie using the provided query.

    Args:
        query (str): The search query.
        payload (dict): The payload containing the JWT token.

    Returns:
        dict: The JSON response containing the search results.
    """
    url = f"https://api.themoviedb.org/3/search/movie?query={query}&include_adult=false&language=en-US&page=1"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {settings.TMDB_BEARER}",
    }

    response = requests.get(url, headers=headers, timeout=10)

    return response.json()


@app.get("/search/tv/{query}")
def search_tv_shows(query: str, payload: dict = Depends(validate_jwt)):
    """
    Search for tv show using the provided query.

    Args:
        query (str): The search query.
        payload (dict): The payload containing the JWT token.

    Returns:
        dict: The JSON response containing the search results.
    """
    url = f"https://api.themoviedb.org/3/search/tv?query={query}&include_adult=false&language=en-US&page=1"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {settings.TMDB_BEARER}",
    }

    response = requests.get(url, headers=headers, timeout=10)

    return response.json()


@app.get("/search/all/{query}")
def search_media(query: str, payload: dict = Depends(validate_jwt)):
    """
    Search for media using the provided query.

    Args:
        query (str): The search query.
        payload (dict): The payload containing the JWT token.

    Returns:
        dict: The JSON response containing the search results.
    """
    url = f"https://api.themoviedb.org/3/search/multi?query={query}&include_adult=false&language=en-US&page=1"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {settings.TMDB_BEARER}",
    }

    response = requests.get(url, headers=headers, timeout=10)

    return response.json()


@app.get("/allReviews/")
async def get_all_reviews(db: Session = Depends(get_db)):
    """
    Retrieve all reviews from the database.

    Args:
        db (Session, optional): SQLAlchemy database session.

    Returns:
        list: A list of all reviews.
    """
    db_response = db.query(Review).all()
    return db_response


@app.post("/reviews/", response_model=ReviewResponse)
async def create_review(
    review_data: ReviewCreate,
    payload: dict = Depends(validate_jwt),
    db: Session = Depends(get_db),
):
    """
    Create a new review.

    Args:
        review_data (ReviewCreate): The data for the new review.
        payload (dict): The payload from the JWT token.
        db (Session): The database session.

    Returns:
        Review: The newly created review.

    Raises:
        HTTPException: If the user ID is not found or if a review already exists for the user and media.
    """
    # TODO: This chunch of code is repeated in multiple places. Refactor it into a function.
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User ID not found."
        )

    existing_review = (
        db.query(Review)
        .filter(Review.User == user_id, Review.MediaId == review_data.MediaId)
        .first()
    )

    if existing_review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A review by user {user_id} for media {review_data.MediaId} already exists.",
        )

    new_review = Review(
        User=user_id,
        stars=review_data.stars,
        ReviewText=review_data.ReviewText,
        MediaId=review_data.MediaId,
        Date=datetime.datetime.now(datetime.timezone.utc),
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


@app.get("/reviews/{media_id}", response_model=list[ReviewByMediaResponse])
async def get_reviews_by_media_id(media_id: int, db: Session = Depends(get_db)):
    """
    Retrieve reviews for a specific media ID from the database.

    Args:
        media_id (int): The ID of the media to fetch reviews for.
        db (Session): SQLAlchemy database session.

    Returns:
        list[ReviewByMediaResponse]: A list of reviews for the specified media ID.
    """
    db_response = (
        db.query(
            Review.id,
            Review.stars,
            Review.ReviewText,
            Review.Date,
            Review.MediaId,
            User.DisplayName,
            User.ProfilePictureUrl,
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
            ProfilePictureUrl=review.ProfilePictureUrl,
        )
        for review in db_response
    ]

    return result


@app.post("/signup/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user in the database.

    Args:
        user (UserCreate): The user data to create.
        db (Session): SQLAlchemy database session.

    Raises:
        HTTPException: If the user already exists.

    Returns:
        User: The created user data.
    """
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


@app.post("/login/")
def login_user(
    email: str = Header(None),
    password: str = Header(None),
    db: Session = Depends(get_db),
):
    """
    Authenticate a user and return a JWT token.

    Args:
        email (str): The email of the user trying to log in.
        password (str): The password of the user trying to log in.
        db (Session): SQLAlchemy database session.

    Raises:
        HTTPException: If authentication fails.

    Returns:
        dict: A JWT token for the authenticated user.
    """
    if email is None or password is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password must be provided in the header.",
        )

    user = db.query(User).filter(User.Email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email {email} not found.",
        )

    if not bcrypt.checkpw(password.encode("utf-8"), user.PasswordHash.encode("utf-8")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password."
        )

    JWT = generate_jwt(user.id)  # type: ignore
    return {"jwt": JWT}


@app.get("/averageRating/{media_id}")
def get_average_rating(media_id: int, db: Session = Depends(get_db)):
    """
    Retrieve the average rating for a specific media ID from the database.
    Return a JSON object if the average rating exists, else return a 404 error.

    Args:
        media_id (int): The ID of the media to fetch the average rating for.
        db (Session): SQLAlchemy database session.

    Returns:
        JSON object with the average rating or a 404 error if no ratings found.
    """
    average_rating = (
        db.query(func.avg(Review.stars)).filter(Review.MediaId == media_id).scalar()
    )

    if average_rating is None:
        raise HTTPException(
            status_code=404, detail=f"No ratings found for media ID {media_id}"
        )

    return {"average_rating": float(average_rating)}


# This is the first protected route in the app.
# It requires a valid JWT as an auth header to access it.
@app.get("/myReviews", response_model=list[ReviewResponse])
def get_my_reviews(
    payload: dict = Depends(validate_jwt), db: Session = Depends(get_db)
):
    """
    Get all the reviews by the user.

    Returns:
        list: A list of all reviews by the user.
    """
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User ID not found."
        )
    reviews = db.query(Review).filter(Review.User == user_id).all()
    if not reviews:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No reviews found."
        )

    return reviews


@app.post("/follow/", status_code=status.HTTP_201_CREATED)
def create_follow(
    follow: FollowCreate,
    payload: dict = Depends(validate_jwt),
    db: Session = Depends(get_db),
):
    """
    Create a new follow relationship between two users.

    Args:
        follow (FollowCreate): The follow object containing the ID of the user to follow.
        payload (dict): The payload extracted from the JWT token.
        db (Session): The database session.

    Returns:
        dict: A json object with a success message if the follow operation is successful.

    Raises:
        HTTPException: If the user ID is not found or if the user is already being followed.
        HTTPException: If there is an internal server error during the database operation.
    """
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User ID not found."
        )

    existing_follow = (
        db.query(Follow)
        .filter(
            Follow.followerId == user_id,
            Follow.followedId == follow.idToFollow,
        )
        .first()
    )

    if existing_follow:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already follow this user.",
        )

    db_follow = Follow(followerId=user_id, followedId=follow.idToFollow)
    db.add(db_follow)
    try:
        db.commit()
        db.refresh(db_follow)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    return {"message": "Follow successful"}


@app.delete("/unfollow/", status_code=status.HTTP_200_OK)
def unfollow_user(
    followedId: int,
    payload: dict = Depends(validate_jwt),
    db: Session = Depends(get_db),
):
    """
    Unfollows a user by deleting the follow relationship from the database.

    Args:
        followedId (int): The ID of the user to unfollow.
        payload (dict, optional): The payload containing the user ID. Required for unfollowing.
        db (Session, optional): The database session.
    Returns:
        dict: An object with a message indicating the unfollow was successful.
    """
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User ID not found."
        )

    follow_relationship = (
        db.query(Follow)
        .filter(Follow.followerId == user_id, Follow.followedId == followedId)
        .first()
    )

    if not follow_relationship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Follow relationship does not exist.",
        )

    try:
        db.delete(follow_relationship)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

    return {"message": "Unfollow successful"}
