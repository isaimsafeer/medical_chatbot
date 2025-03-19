const chatBody = document.querySelector(".chat-body");
const chatForm = document.querySelector(".chat-form");
const messageInput = document.querySelector(".message-input");
const closeChatbot = document.getElementById("close-chatbot");

let ws = null;

// Initialize WebSocket connection
function initWebSocket() {
  ws = new WebSocket("ws://localhost:8000/ws");

  ws.onopen = () => {
    console.log("WebSocket connected.");
  };

  ws.onmessage = (event) => {
    const message = event.data;
    addMessage(message, "bot");
  };

  ws.onclose = () => {
    console.log("WebSocket disconnected. Attempting to reconnect...");
    setTimeout(initWebSocket, 2000);
  };

  ws.onerror = (err) => {
    console.error("WebSocket error:", err);
    ws.close();
  };
}

// Function to add messages to chat window
function addMessage(message, sender) {
  const messageDiv = document.createElement("div");
  messageDiv.classList.add("message");
  messageDiv.classList.add(sender === "bot" ? "bot-message" : "user-message");

  if (sender === "bot") {
    messageDiv.innerHTML = `
      <img class="chatbot-logo" src="/static/images/robotic.png" alt="Chatbot Logo" width="50" height="50">
      <div class="message-text">${message.replace(/\n/g, "<br>")}</div>
    `;
  } else {
    messageDiv.innerHTML = `
      <div class="message-text user-text">${message.replace(/\n/g, "<br>")}</div>
    `;
  }

  chatBody.appendChild(messageDiv);
  chatBody.scrollTop = chatBody.scrollHeight;
}

// Form submission handler
chatForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const message = messageInput.value.trim();
  if (!message) return;

  addMessage(message, "user");

  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({ message: message }));
  } else {
    addMessage("Error: WebSocket connection is closed.", "bot");
  }

  messageInput.value = "";
});

// Close chatbot button toggle (optional if you want to hide/show)
closeChatbot.addEventListener("click", () => {
  document.querySelector(".chatbot-popup").classList.toggle("hidden");
});

// Start WebSocket connection on load
initWebSocket();
