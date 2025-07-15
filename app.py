from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import RedirectResponse
import numpy as np
import joblib
import uvicorn
import os

app = FastAPI()

model = joblib.load("model.pkl")

# class Input(BaseModel):
#     features: list[float]

class Input(BaseModel):
    Cycle_Index: float
    Discharge Time (s): float
    Decrement 3.6-3.4V (s): float
    Max. Voltage Dischar. (V): float
    Min. Voltage Charg. (V): float
    Time at 4.15V (s): float
    Time constant current (s): float
    Charging time (s): float


@app.post("/predict")
def predict(input: Input):
    #data = np.array([input.features])
    data = np.array([[
        input.Cycle_Index, 
        input.Discharge Time (s), 
        input.Decrement 3.6-3.4V (s), 
        input.Max. Voltage Dischar. (V),
        input.Min. Voltage Charg. (V),
        input.Time at 4.15V (s),
        input.Time constant current (s),
        input.Charging time (s)]])
    prediction = model.predict(data)
    return {"prediction": int(prediction[0])}


@app.get("/")
def root():
    return RedirectResponse(url="/docs")
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)


Cycle_Index	Discharge Time (s)						