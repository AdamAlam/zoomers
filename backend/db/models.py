from sqlalchemy import TIMESTAMP, Boolean, Column, Float, ForeignKey, Integer, String

from .session import Base


class User(Base):
    """
    Represents a user in the system.

    Attributes:
        id (int): The unique identifier for the user.
        Username (str): The username of the user.
        Email (str): The email address of the user.
        PasswordHash (str): The hashed password of the user.
        DisplayName (str): The display name of the user.
        Bio (str): The biography of the user.
        ProfilePictureUrl (str): The URL of the user's profile picture.
        IsPrivate (bool): Indicates whether the user's profile is private or not.
        FirstName (str): The first name of the user.
        LastName (str): The last name of the user.
    """

    __tablename__ = "User"

    id = Column(Integer, primary_key=True, index=True)
    Username = Column(String, unique=True, index=True)
    Email = Column(String, unique=True, index=True)
    PasswordHash = Column(String)
    DisplayName = Column(String)
    Bio = Column(String)
    ProfilePictureUrl = Column(String)
    IsPrivate = Column(Boolean)
    FirstName = Column(String)
    LastName = Column(String)


class Follow(Base):
    """
    Represents a follow relationship between users.

    Attributes:
        id (int): The unique identifier for the follow relationship.
        followerId (int): The ID of the user who is following.
        followedId (int): The ID of the user who is being followed.
    """

    __tablename__ = "Follow"

    id = Column(Integer, primary_key=True, index=True)
    followerId = Column(Integer, ForeignKey("User.id"))
    followedId = Column(Integer, ForeignKey("User.id"))


class Review(Base):
    """
    Represents a review of a media item by a user.

    Attributes:
        id (int): The unique identifier for the review.
        User (int): The ID of the user who wrote the review.
        stars (float): The rating given to the media item.
        ReviewText (str): The text of the review.
        Date (datetime): The date and time when the review was created.
        MediaId (int): The ID of the media item being reviewed.
    """

    __tablename__ = "Review"
    id = Column(Integer, primary_key=True, index=True)
    User = Column(Integer, ForeignKey("User.id"))
    stars = Column(Float)
    ReviewText = Column(String)
    Date = Column(TIMESTAMP)
    MediaId = Column(Integer)


class Watched(Base):
    """
    Represents a media item that a user has watched.

    Attributes:
        id (int): The unique identifier for the watched item.
        user_id (int): The ID of the user who watched the item.
        media_id (int): The ID of the watched media item.
        created_at (datetime): The date and time when the item was watched.
    """

    __tablename__ = "Watched"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("User.id"))
    media_id = Column(Integer)
    created_at = Column(TIMESTAMP)
