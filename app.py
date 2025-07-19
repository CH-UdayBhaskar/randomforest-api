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


app = FastAPI()

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


@app.get("/")
def root():
    return RedirectResponse(url="/docs")
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)

import streamlit.components.v1 as components

chatbot_widget = """
<style>
#chatbot-button {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background-color: #0084ff;
  color: white;
  border: none;
  border-radius: 30px;
  padding: 10px 16px;
  font-size: 16px;
  z-index: 9999;
  cursor: pointer;
}
#chatbot-container {
  position: fixed;
  bottom: 80px;
  right: 20px;
  width: 300px;
  max-height: 400px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
  display: none;
  flex-direction: column;
  z-index: 9999;
  font-family: sans-serif;
}
#chatbot-header {
  background-color: #0084ff;
  color: white;
  padding: 10px;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  font-weight: bold;
}
#chatbot-messages {
  padding: 10px;
  height: 250px;
  overflow-y: auto;
  font-size: 14px;
}
#chatbot-input {
  display: flex;
  border-top: 1px solid #ccc;
}
#chatbot-input textarea {
  flex: 1;
  padding: 10px;
  border: none;
  resize: none;
  height: 40px;
}
#chatbot-input button {
  background-color: #0084ff;
  color: white;
  border: none;
  padding: 0 16px;
  cursor: pointer;
}
</style>

<button id="chatbot-button">💬 Chat</button>

<div id="chatbot-container">
  <div id="chatbot-header">AI Assistant</div>
  <div id="chatbot-messages"></div>
  <div id="chatbot-input">
    <textarea id="user-input" placeholder="Ask something..."></textarea>
    <button onclick="sendMessage()">Send</button>
  </div>
</div>

<script>
document.getElementById("chatbot-button").onclick = function () {
  const bot = document.getElementById("chatbot-container");
  bot.style.display = bot.style.display === "none" ? "flex" : "none";
};

async function sendMessage() {
  const input = document.getElementById("user-input");
  const message = input.value.trim();
  if (!message) return;

  const messagesBox = document.getElementById("chatbot-messages");
  messagesBox.innerHTML += "<div><b>You:</b> " + message + "</div>";

  input.value = "";

  try {
    const response = await fetch("https://randomforest-api.onrender.com/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
    });

    const data = await response.json();
    const reply = data.response || "Sorry, I couldn't respond.";
    messagesBox.innerHTML += "<div><b>Bot:</b> " + reply + "</div>";
    messagesBox.scrollTop = messagesBox.scrollHeight;
  } catch (err) {
    messagesBox.innerHTML += "<div><b>Bot:</b> Error contacting server.</div>";
  }
}
</script>
"""

components.html(chatbot_widget, height=600)

						