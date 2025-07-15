from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import joblib
import uvicorn
import os

app = FastAPI()

model = joblib.load("model.pkl")

class Input(BaseModel):
    features: list[float]

@app.post("/predict")
def predict(input: Input):
    data = np.array([input.features])
    prediction = model.predict(data)
    return {"prediction": int(prediction[0])}

@app.get("/")
def home():
    return {"message": "Welcome to RandomForest API! Visit /docs"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)
