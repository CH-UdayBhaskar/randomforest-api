from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import RedirectResponse
from typing import Dict
import numpy as np
import joblib
import uvicorn
import os

app = FastAPI()

model = joblib.load("model.pkl")

# class Input(BaseModel):
#     features: list[float]

class Input(BaseModel):
    features: Dict[str, float]

column_names=["Cycle_Index",	"Discharge Time (s)",	"Decrement 3.6-3.4V (s)",	"Max. Voltage Dischar. (V)",	"Min. Voltage Charg. (V)",	"Time at 4.15V (s)",	"Time constant current (s)",	"Charging time (s)"]

@app.post("/predict")
def predict(input: Input):
    #data = np.array([input.features])
    values=[input.features[col] for col in column_names]
    data = np.array([values])
    prediction = model.predict(data)
    return {"prediction": int(prediction[0])}


@app.get("/")
def root():
    return RedirectResponse(url="/docs")
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)


						