from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.models.meal import Meal
from app.schemas.food import FoodAnalysisResponse, MealResponse
from app.services.ai_agent import FoodAgent
from typing import Optional

router = APIRouter(
    prefix="/food",
    tags=["food"]
)

agent = FoodAgent()

@router.post("/analyze/{user_id}", response_model=FoodAnalysisResponse)
async def analyze_food(
    user_id: int,
    image: UploadFile = File(...),
    mode: Optional[str] = "consult",
    db: Session = Depends(get_db)
):
    # Step 1 — fetch user from database
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Step 2 — read image bytes
    image_bytes = await image.read()

    # Step 3 — run the agent
    analysis = agent.analyze(
        image_bytes=image_bytes,
        user_goal=user.goal,
        daily_calories=user.daily_calories,
        mode=mode
    )

    # Step 4 — save meal to database if mode is log
    if mode == "log":
        meal = Meal(
            user_id=user_id,
            description=analysis.description,
            calories=analysis.total_calories,
            protein=analysis.total_protein,
            carbs=analysis.total_carbs,
            fats=analysis.total_fats,
            advice=analysis.advice
        )
        db.add(meal)
        db.commit()
        db.refresh(meal)

    return analysis


@router.get("/history/{user_id}", response_model=list[MealResponse])
def get_meal_history(
    user_id: int,
    db: Session = Depends(get_db)
):
    # check user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # fetch all meals for this user
    meals = db.query(Meal).filter(Meal.user_id == user_id).all()
    return meals