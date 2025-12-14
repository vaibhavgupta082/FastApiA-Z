from .. import models
from sqlalchemy.orm import Session
from ..schemas import ShowBlog, Blog, BlogBase
from fastapi import HTTPException, status
from .. import hashing
from ..schemas import User, TripRequest


def get_trip_by_user(db: Session, user_id: int):
    trips = db.query(models.Trip).filter(models.Trip.user_id == user_id).all()
    return trips

def create_trip_entry(db: Session, request: TripRequest, user_id: int):
    trip = models.Trip(
        user_id=user_id,

        source=request.source,
        destination=request.destination,
        start_date=request.start_date,
        days=request.days,
        people=request.people,
        budget=request.budget,
        currency=request.currency,

        travel_type=request.travel_type,
        travel_mode=request.travel_mode,
        accommodation_type=request.accommodation_type,
        diet=request.diet,
        pace=request.pace,
        occasion=request.occasion,

        interests=request.interests,           # JSON
        request_payload=request.dict(),         # Full snapshot

        status="IN_PROGRESS"
    )

    db.add(trip)
    db.commit()
    db.refresh(trip)

    return trip

def update_trip_plan(db: Session, trip_id: int, trip_plan: dict):
    trip = db.query(models.Trip).filter(models.Trip.id == trip_id).first()

    trip.trip_plan = trip_plan
    trip.status = "COMPLETED"

    db.commit()
    db.refresh(trip)
    return trip