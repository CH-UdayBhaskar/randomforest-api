from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.responses import RedirectResponse
from typing import Dict
import numpy as np
import joblib
import uvicorn
import os
import pandas as pd

app = FastAPI()

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


@app.get("/")
def root():
    return RedirectResponse(url="/docs")
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)


						
