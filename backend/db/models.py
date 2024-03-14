from .session import Base
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, Float, TIMESTAMP


class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    Username = Column(String, unique=True, index=True)
    PasswordHash = Column(String)
    DisplayName = Column(String)
    Bio = Column(String)
    ProfilePictureUrl = Column(String)
    IsPrivate = Column(Boolean)
    FirstName = Column(String)
    LastName = Column(String)


class Follow(Base):
    __tablename__ = "Follow"

    id = Column(Integer, primary_key=True, index=True)
    FollowerId = Column(Integer, ForeignKey("User.id"))
    FolloweeId = Column(Integer, ForeignKey("User.id"))


class Review(Base):
    __tablename__ = "Review"
    id = Column(Integer, primary_key=True, index=True)
    User = Column(Integer, ForeignKey("User.id"))
    stars = Column(Float)
    ReviewText = Column(String)
    Date = Column(TIMESTAMP)
    MediaId = Column(Integer)
