from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ..database import get_db
from ..schemas import ShowBlog, Blog, BlogBase , User, PromptRequest
from .. import models
from sqlalchemy.orm import Session
from .. repository.Blog import get_all, create, get_by_id, delete , update
from .. import Oauth2
import google.generativeai as genai
import os
from ..prompts import trippy_prompt


router = APIRouter(tags=["Trippy"], prefix="/trip")

my_api_key = 'x'

genai.configure(api_key=my_api_key)

# Choose model (flash = fast, pro = deep reasoning)
model = genai.GenerativeModel("gemini-1.5-flash")

@router.post("/generate")
async def generate_text(request: PromptRequest, current_user : User = Depends(Oauth2.get_current_user)):
    """
    Receives a prompt and returns the AI-generated text.
    """
    try:
        trippy_prompt_filled = (
            trippy_prompt
            .replace("{{SOURCE}}", str(request.Source))
            .replace("{{DESTINATION}}", str(request.Destination))
            .replace("{{DAYS}}", str(request.Days))
            .replace("{{PEOPLE}}", str(request.People))
            .replace("{{BUDGET}}", str(request.Budget))
            .replace("{{MONTH}}", str(request.Month))
        )
        
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(trippy_prompt_filled)
        return {"response": response.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
def blog():
    return {"data": "This is trippy router"}