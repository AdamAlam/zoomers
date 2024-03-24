from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserSchema(BaseModel):
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
    User: int
    stars: float
    ReviewText: str
    Date: str
    MediaId: int

    class Config:
        orm_mode = True


class ReviewCreate(BaseModel):
    stars: float
    ReviewText: str
    MediaId: int


class ReviewResponse(BaseModel):
    id: int
    User: int
    stars: float
    ReviewText: str
    Date: datetime
    MediaId: int

    class Config:
        orm_mode = True


class ReviewByMediaResponse(BaseModel):
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
    idToFollow: int
