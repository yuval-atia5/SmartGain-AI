from google import genai
from google.genai import types
from app.schemas.food import FoodAnalysisResponse, FoodItem
from dotenv import load_dotenv
from PIL import Image
import os
import json
import io

load_dotenv()

class FoodAgent:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = "gemini-2.5-flash"

    def analyze(self, image_bytes: bytes, user_goal: str, daily_calories: int, mode: str = "consult") -> FoodAnalysisResponse:
        # Step 1 — convert bytes to image
        img = Image.open(io.BytesIO(image_bytes))

        # Step 2 — build the prompt based on mode
        prompt = self._build_prompt(user_goal, daily_calories, mode)

        # Step 3 — send image + prompt to Gemini
        response = self.client.models.generate_content(
            model=self.model,
            contents=[prompt, img],
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )

        # Step 4 — parse the response
        raw = json.loads(response.text)

        # Step 5 — validate and return structured response
        return FoodAnalysisResponse(
            description=raw["description"],
            user_summary=raw["user_summary"],
            items=[FoodItem(**item) for item in raw["items"]],
            total_calories=raw["total_calories"],
            total_protein=raw["total_protein"],
            total_carbs=raw["total_carbs"],
            total_fats=raw["total_fats"],
            advice=raw["advice"]
        )

    def _build_prompt(self, user_goal: str, daily_calories: int, mode: str) -> str:
        if mode == "consult":
            advice_instruction = f"""
            The user has NOT eaten this yet. They want to know if they SHOULD eat it.
            Give proactive advice:
            - Will this food help them reach their goal of {user_goal}?
            - Does it fit their daily calorie target of {daily_calories} calories?
            - What specific ingredients should they remove or add?
            - Give a clear YES or NO recommendation with a reason.
            Example: "This meal is high in protein which fits your muscle building goal, 
            but the fries add empty calories. Swap them for rice to maximize gains."
            """
        else:  # mode == "log"
            advice_instruction = f"""
            The user already ate this meal. Give reflective advice:
            - How did this meal affect their goal of {user_goal}?
            - How many calories remain in their daily target of {daily_calories} calories?
            - What should their next meal look like to balance this one?
            Example: "You consumed 850 calories. You have 1150 remaining today. 
            Your next meal should be high in protein and low in carbs to stay on track."
            """

        return f"""
        You are a clinical nutritionist AI analyzing a food image.
        
        The user's health goal is: {user_goal}
        Their daily calorie target is: {daily_calories} calories.
        Mode: {"Pre-meal consultation" if mode == "consult" else "Post-meal logging"}
        
        Analyze every food item visible in this image.
        
        Return a JSON object with exactly these fields:
        {{
            "description": "brief description of the full meal",
            "user_summary": "friendly 2-3 sentence summary for the user",
            "items": [
                {{
                    "name": "food item name",
                    "calories": 000,
                    "protein": 00,
                    "carbs": 00,
                    "fats": 00
                }}
            ],
            "total_calories": 000,
            "total_protein": 00,
            "total_carbs": 00,
            "total_fats": 00,
            "advice": "{advice_instruction}"
        }}
        
        Return only valid JSON, no extra text.
        """