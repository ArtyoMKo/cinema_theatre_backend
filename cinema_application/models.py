from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from cinema_application.database import Base, relationship


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)

    def update(self, **kwargs):
        for field, value in kwargs.items():
            if value is not None:
                setattr(self, field, value)

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    seats = Column(Integer)
    sessions = relationship("MovieSession", back_populates="movie_sessions")

    def update(self, **kwargs):
        for field, value in kwargs.items():
            if value is not None:
                setattr(self, field, value)

class MovieSession(Base):
    __tablename__ = "movie_sessions"

    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    movie_id = Column(Integer, ForeignKey("movies.id"))
    room_id = Column(Integer, ForeignKey("rooms.id"))
    room = relationship("Room", back_populates="rooms")
    movie = relationship("Movie", back_populates="movies")

    def update(self, **kwargs):
        for field, value in kwargs.items():
            if value is not None:
                setattr(self, field, value)

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    duration = Column(Integer)
    movie_sessions = relationship("MovieSession", back_populates="movie_sessions")


class Reservation(Base):
    __tablename__ = (
        "reservations"  # For help sqlalchemy to know what is the name of table later on
    )

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    priority = Column(Integer, nullable=False)
    complete = Column(Boolean, default=False)
    session_id = Column(Integer, ForeignKey("movie_sessions.id"))
    sessions = relationship("MovieSession", back_populates="movie_sessions")

    def update(self, **kwargs):
        for field, value in kwargs.items():
            if value is not None:
                setattr(self, field, value)
