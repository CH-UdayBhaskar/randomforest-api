from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import joblib

app = FastAPI()

model = joblib.load("model_1.pkl")

class Input(BaseModel):
    features: list[float]

@app.post("/predict")
def predict(input: Input):
    data = np.array([input.features])
    prediction = model.predict(data)
    return {"prediction": int(prediction[0])}
