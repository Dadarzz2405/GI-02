const chatToggle = document.getElementById("chat-toggle");
const chatBox = document.getElementById("chat-box");
const chatClose = document.getElementById("chat-close");
const sendBtn = document.getElementById("send-btn");
const input = document.getElementById("user-input");
const messages = document.getElementById("chat-messages");

let greeted = false;

// Open chat
chatToggle.onclick = () => {
  chatBox.style.display = "flex";

  // AI sends first message (only once per page load)
  if (!greeted) {
    addMessage(
      "bot",
      "Assalamu’alaikum. I can help explain features or guide you to pages like attendance or dashboard."
    );
    greeted = true;
  }
};

// Close chat
chatClose.onclick = () => {
  chatBox.style.display = "none";
};

// Add message to UI
function addMessage(role, text) {
  const div = document.createElement("div");
  div.className =
    role === "user"
      ? "message-wrapper user-msg"
      : "message-wrapper bot-msg";
  div.textContent = text;
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
}

// Send on button or Enter
sendBtn.onclick = sendMessage;
input.addEventListener("keypress", e => {
  if (e.key === "Enter") sendMessage();
});

function sendMessage() {
  const text = input.value.trim();
  if (!text) return;

  addMessage("user", text);
  input.value = "";

  fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: text })
  })
    .then(res => res.json())
    .then(data => {
      // Navigation intent
      if (data.action === "navigate" && data.redirect) {
        addMessage("bot", "Taking you there...");
        setTimeout(() => {
          window.location.href = data.redirect;
        }, 800);
      }
      // Normal chat reply
      else if (data.action === "chat") {
        addMessage("bot", data.message);
      }
      // Fallback safety
      else {
        addMessage("bot", "I'm sorry, I didn't understand that.");
      }
    })
    .catch(() => {
      addMessage("bot", "Error contacting server.");
    });
}
