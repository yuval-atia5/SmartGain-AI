from pydantic import BaseModel
from datetime import datetime

class FoodItem(BaseModel):
    name: str
    calories: int
    protein: int
    carbs: int
    fats: int

class FoodAnalysisResponse(BaseModel):
    description: str
    user_summary: str
    items: list[FoodItem]
    total_calories: int
    total_protein: int
    total_carbs: int
    total_fats: int
    advice: str

class MealResponse(BaseModel):
    id: int
    description: str
    calories: int
    protein: int
    carbs: int
    fats: int
    advice: str
    created_at: datetime

    class Config:
        from_attributes = True