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
from sqlalchemy.orm import Session
from util.generateJWT import generate_jwt
import jwt


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

@app.get("/searchMovie/")
async def search_movie(query: str):
    """
    Search for a movie by query string and return the movie details from an external API.

    Args:
     query (str): The query string to search for a movie.

    Returns:
        dict: The movie details as a JSON response.
    """
    print(query)
    url = f"https://api.themoviedb.org/3/search/movie?language=en-US&query={query}"
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
async def create_review(review_data: ReviewCreate, db: Session = Depends(get_db)):
    """
    Create a new review in the database.

    Args:
        review_data (ReviewCreate): The review data to create.
        db (Session): SQLAlchemy database session.

    Raises:
        HTTPException: If the review already exists.

    Returns:
        ReviewResponse: The created review data.
    """
    print(review_data)
    
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

    JWT = generate_jwt(user.id)
    return {"jwt": JWT}


# TODO: We might need to start only allowing these requests to go through
#  if the JWT is valid and the user is authenticated.
@app.post("/follow/", status_code=status.HTTP_201_CREATED)
def create_follow(follow: FollowCreate, db: Session = Depends(get_db)):
    """
    Create a new follow relationship between two users.

    Args:
        follow (FollowCreate): The follow relationship to be created.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        dict: A dictionary containing a success message.

    Raises:
        HTTPException: If the follow relationship already exists or if there is an internal server error.
    """
    existing_follow = (
        db.query(Follow)
        .filter(
            Follow.followerId == follow.followerId,
            Follow.followedId == follow.followedId,
        )
        .first()
    )

    if existing_follow:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already follow this user.",
        )

    db_follow = Follow(followerId=follow.followerId, followedId=follow.followedId)
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


# TODO: We might need to start only allowing these requests to go through
#  if the JWT is valid and the user is authenticated.
@app.delete("/unfollow/", status_code=status.HTTP_200_OK)
def unfollow_user(followerId: int, followedId: int, db: Session = Depends(get_db)):
    """
    Unfollows a user by deleting the follow relationship from the database.

    Args:
        followerId (int): The ID of the follower user.
        followedId (int): The ID of the user being followed.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        dict: A dictionary containing a success message.

    Raises:
        HTTPException: If the follow relationship does not exist or if there is an internal server error.
    """
    follow_relationship = (
        db.query(Follow)
        .filter(Follow.followerId == followerId, Follow.followedId == followedId)
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

@app.get("/ownReviews", response_model=list[ReviewByMediaResponse])
async def get_own_reviews(jwtToken: str = Header(None), db: Session = Depends(get_db)):
    """
    TODO: Add docstring
    """
    print(jwtToken)
    if jwtToken is None :
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User JWT token must be provided in the header.",
        )
    decoded_jwt = jwt.decode(jwtToken, settings.JWT_SECRET, algorithms=["HS256"])
    print(decoded_jwt)
    user_id = decoded_jwt["user_id"]

    db_response = (
        db.query(
            Review.id,
            Review.stars,
            Review.ReviewText,
            Review.Date,
            Review.MediaId,
            User.DisplayName,
        )
        .join(User, User.id == Review.User)
        .filter(User.id == user_id)
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