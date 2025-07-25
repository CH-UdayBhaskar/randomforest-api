from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
import numpy as np
import joblib
import uvicorn
import os
from chatbot import router as chatbot_router
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse




app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For now, allow all origins (adjust for security)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include chatbot router
app.include_router(chatbot_router)

model = joblib.load("model.pkl")

# class Input(BaseModel):
#     features: list[float]

class Input(BaseModel):
    cycle_index: float = Field(..., alias="Cycle_Index")
    discharge_time: float = Field(..., alias="Discharge Time (s)")
    decrement: float = Field(..., alias="Decrement 3.6-3.4V (s)")
    max_voltage: float = Field(..., alias="Max. Voltage Dischar. (V)")
    min_voltage: float = Field(..., alias="Min. Voltage Charg. (V)")
    time_at_4_15v: float = Field(..., alias="Time at 4.15V (s)")
    time_constant: float = Field(..., alias="Time constant current (s)")
    charging_time: float = Field(..., alias="Charging time (s)")

    class Config:
        allow_population_by_field_name = True  # enables alias usage

@app.post("/predict")
def predict(input: Input):
    #data = np.array([input.features])
    #values=[input.features[col] for col in column_names]
    data = np.array([[
        input.cycle_index,
        input.discharge_time,
        input.decrement,
        input.max_voltage,
        input.min_voltage,
        input.time_at_4_15v,
        input.time_constant,
        input.charging_time
    ]])
    prediction = model.predict(data)
    return {"prediction": int(prediction[0])}



@app.get("/", include_in_schema=False)
async def custom_swagger_ui_html():
    with open("static/swagger.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)


# @app.get("/")
# def root():
#     return RedirectResponse(url="/docs")
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)


						