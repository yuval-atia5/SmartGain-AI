from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    goal: str
    daily_calories: int

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    goal: str
    daily_calories: int

    class Config:
        from_attributes = True