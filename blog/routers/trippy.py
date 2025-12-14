from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ..database import get_db
from ..schemas import ShowBlog, Blog, BlogBase , User, TripRequest
from .. import models
from sqlalchemy.orm import Session
from .. repository.Blog import get_all, create, get_by_id, delete , update
from .. repository.trippy import get_trip_by_user, create_trip_entry, update_trip_plan
from .. repository.User import get_by_email
from .. import Oauth2
import google.generativeai as genai
import os
from .. prompts.test_prompt import test_trippy_prompt as test_prompt
from .. prompts.prompts import trippy_prompt
from .. core.config import settings


router = APIRouter(tags=["Trippy"], prefix="/trip")

my_api_key = settings.GEMINI_API_KEY
genai.configure(api_key=my_api_key)

# Choose model (flash = fast, pro = deep reasoning)
model = genai.GenerativeModel("gemini-1.5-flash")

@router.post("/generate")
async def generate_trip_plan(
    request: TripRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(Oauth2.get_current_user)
):
    trip = None  # ✅ important
    print("Generating trip plan for user:", current_user.email)
    user = get_by_email(db,current_user.email)  # Ensure user exists
    print("User ID:", user.id)
    try:
        
        trippy_prompt_filled = (
            trippy_prompt
            .replace("{{SOURCE}}", request.source)
            .replace("{{DESTINATION}}", request.destination)
            .replace("{{START_DATE}}", request.start_date or "Not specified")
            .replace("{{DAYS}}", str(request.days))
            .replace("{{PEOPLE}}", request.people)
            .replace("{{AGES}}", request.ages or "Not specified")
            .replace("{{BUDGET}}", request.budget)
            .replace("{{CURRENCY}}", request.currency)
            .replace("{{TRAVEL_TYPE}}", request.travel_type or "Not specified")
            .replace("{{TRAVEL_MODE}}", request.travel_mode)
            .replace("{{ACCOMMODATION_TYPE}}", request.accommodation_type or "Hotel")
            .replace("{{DIET}}", request.diet)
            .replace("{{PACE}}", request.pace)
            .replace("{{OCCASION}}", request.occasion)
            .replace("{{MUST_DO}}", request.must_do)
            .replace("{{AVOID}}", request.avoid)
            .replace("{{MOBILITY}}", request.mobility)
            .replace("{{NATIONALITY}}", request.nationality or "Not specified")
            .replace("{{INTERESTS}}", ", ".join(request.interests) if request.interests else "General sightseeing")

        )
        print("request prepared for model:", request)
        print("user_id prepared for model:", user.id)
        trip = create_trip_entry(
            db=db,
            request=request,
            user_id=user.id
        )
        print("Trip entry created with ID:", trip.id)
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(trippy_prompt_filled)

        # 4️⃣ Update same trip row
        update_trip_plan(
            db=db,
            trip_id=trip.id,
            trip_plan=response.text
        )

        return {
                "success": True,
                "user": current_user.email,
                "trip_plan": response.text
            }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Trip generation failed: {str(e)}"
        )

# @router.get("/")
# def blog():
#     return {"data": "This is trippy router"}
# @router.get("/get_current_user")
# def get_current_user(
#     token: str = Depends(oauth2_scheme),
#     db: Session = Depends(get_db)
# ):
#     if token is None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Not authenticated"
#         )

#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email: str = payload.get("sub")
#         if email is None:
#             raise HTTPException(status_code=401, detail="Invalid token")
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid token")

#     user = db.query(models.User).filter(models.User.email == email).first()

#     if user is None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="User not found"
#         )

#     return user  # ✅ ALWAYS return a user