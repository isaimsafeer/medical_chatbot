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
    // Check if the message is a user echo or a bot response
    if (message.startsWith("User:")) {
      const userMessage = message.replace("User: ", "");
      addMessage(userMessage, "user");
    } else {
      addMessage(message, "bot");
    }
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

  // Add image based on sender
  const imageSrc = sender === "bot" ? "/static/images/robotic.png" : "/static/images/user.png";
  
  messageDiv.innerHTML = `
    <div class="message-content">
      <img class="chatbot-logo" src="${imageSrc}" alt="${sender} Logo" width="50" height="50">
      <div class="message-text">${message.replace(/\n/g, "<br>")}</div>
    </div>
  `;

  chatBody.appendChild(messageDiv);
  chatBody.scrollTop = chatBody.scrollHeight;
}

// Form submission handler
chatForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const message = messageInput.value.trim();
  if (!message) return;

  // Do NOT add the user message here; let the server handle it
  // addMessage(message, "user"); // Removed to prevent duplication

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