import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Battery RUL Predictor", layout="wide")
st.title("🔋 Battery Life Predictor with AI Assistant")
st.markdown("Ask your assistant anything using the chat bubble in the bottom-right corner.")

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
