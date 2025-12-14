from sqlalchemy import (
    Column, Integer, String, ForeignKey,
    DateTime, JSON
)
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base
from sqlalchemy.sql import func

class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    creator = relationship("User", back_populates="blogs")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

    blogs = relationship("Blog", back_populates="creator")
    trips = relationship("Trip", back_populates="user")

class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Core searchable columns
    source = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    start_date = Column(String, nullable=True)
    days = Column(Integer, nullable=False)
    people = Column(String, nullable=False)
    budget = Column(String, nullable=False)
    currency = Column(String, default="INR")

    # # Optional but useful filters
    travel_type = Column(String, nullable=True)
    travel_mode = Column(String, default="any")
    accommodation_type = Column(String, nullable=True)
    diet = Column(String, default="none")
    pace = Column(String, default="balanced")
    occasion = Column(String, default="none")

    #JSON storage
    interests = Column(JSON, nullable=True)
    request_payload = Column(JSON, nullable=False)
    trip_plan = Column(JSON, nullable=True)

    status = Column(String, default="IN_PROGRESS")

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="trips")