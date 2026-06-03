from fastapi import FastAPI
from app.routers import food, users
from app.db.database import engine, Base

# Create all database tables automatically on startup
Base.metadata.create_all(bind=engine)

# Create the main FastAPI application
app = FastAPI(
    title="SmartGain AI",
    description="AI-powered food analysis agent",
    version="1.0.0"
)

# Connect all routers to the main app
app.include_router(food.router)
app.include_router(users.router)

@app.get("/")
def home():
    return {"message": "SmartGain AI is running"}