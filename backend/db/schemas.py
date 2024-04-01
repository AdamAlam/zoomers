from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserSchema(BaseModel):
    """
    Schema for user data.
    """

    id: int
    email: str
    Username: str
    PasswordHash: str
    DisplayName: str
    Bio: str
    ProfilePictureUrl: str
    IsPrivate: bool
    FirstName: str
    LastName: str

    class Config:
        orm_mode = True


class ReviewSchema(BaseModel):
    """
    Schema for review data.
    """

    User: int
    stars: float
    ReviewText: str
    Date: str
    MediaId: int

    class Config:
        orm_mode = True


class ReviewCreate(BaseModel):
    """
    Schema for creating a review.
    """

    stars: float
    ReviewText: str
    MediaId: int


class ReviewResponse(BaseModel):
    """
    Schema for review response data.
    """

    id: int
    User: int
    stars: float
    ReviewText: str
    Date: datetime
    MediaId: int
    ProfilePictureUrl: Optional[str] = None
    DisplayName: Optional[str] = None

    class Config:
        orm_mode = True


class ReviewByMediaResponse(BaseModel):
    """
    Schema for review response data by media.
    """

    id: int
    stars: float
    ReviewText: str
    Date: datetime
    MediaId: int
    DisplayName: str
    # TODO: 'None' used for null check. Should we default a profile picture when a user a created? Then we don't need the 'None'.
    ProfilePictureUrl: str | None

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    """
    Schema for creating a user.
    """

    Email: str
    Username: str
    Password: str
    DisplayName: str
    Bio: Optional[str] = None
    ProfilePictureUrl: Optional[str] = None
    IsPrivate: Optional[bool] = False
    FirstName: str
    LastName: Optional[str] = None


class FollowCreate(BaseModel):
    """
    Schema for creating a follow relationship.
    """

    idToFollow: int
