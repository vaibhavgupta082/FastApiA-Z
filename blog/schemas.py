from typing import List, Optional
from pydantic import BaseModel , Field


class TripRequest(BaseModel):
    source: str = Field(..., example="Mumbai, India")
    destination: str = Field(..., example="Bali, Indonesia")

    start_date: str = Field(None, example="2025-06-15", description="YYYY-MM-DD")

    days: int = Field(..., example=7, description="Number of full days on-site")
    people: str = Field(..., example="2 adults + 1 child")
    ages: Optional[str] = Field(None, example="adults: 35,38; child: 10")
    budget: str = Field(..., example="2000 USD / 150000 INR / mid")
    currency: Optional[str] = Field("INR", example="USD")
    travel_type: Optional[str] = Field(None, example="family")
    travel_mode: Optional[str] = Field("any", example="flight")
    interests: Optional[List[str]] = Field(None, example=["beaches", "food", "adventure"])
    accommodation_type: Optional[str] = Field(None, example="hotel")

    diet: Optional[str] = Field("none", example="vegetarian")
    pace: Optional[str] = Field("balanced", example="relaxed")

    must_do: Optional[str] = Field("none", example="scuba diving")
    avoid: Optional[str] = Field("none", example="crowds")
    mobility: Optional[str] = Field("none", example="stroller")
    nationality: Optional[str] = Field(None, example="Indian")
    occasion: Optional[str] = Field("none", example="honeymoon")

class BlogBase(BaseModel):
    title: str
    body: str

class Blog(BlogBase):
    class Config():
        orm_mode = True

class User(BaseModel):
    name:str
    email:str
    password:str

class ShowUser(BaseModel):
    name:str
    email:str
    blogs : List[Blog] =[]
    class Config():
        orm_mode = True

class UserCreate(BaseModel):
    name:str
    email:str
    class Config():
        orm_mode = True

class ShowBlog(BaseModel):
    title: str
    body:str
    creator: UserCreate

    class Config():
        orm_mode = True

class Login(BaseModel):
    username: str
    password: str
    class Config():
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None