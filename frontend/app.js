const API = "http://127.0.0.1:8000";
let token = localStorage.getItem("token");

// Auto-login check
if (token) showChat();

async function apiRequest(endpoint, options = {}) {
    const headers = { "Content-Type": "application/json", ...options.headers };
    if (token) headers["Authorization"] = `Bearer ${token}`;

    try {
        const response = await fetch(`${API}${endpoint}`, { ...options, headers });
        
        if (response.status === 401) {
            logout();
            throw new Error("Session expired. Please login again.");
        }
        
        return await response.json();
    } catch (err) {
        console.error("API Error:", err);
        throw err;
    }
}

function showChat() {
    document.getElementById("auth-section").classList.add("hidden");
    document.getElementById("chat-section").classList.remove("hidden");
}

async function login() {
    const btn = document.getElementById("loginBtn");
    btn.disabled = true;

    try {
        const data = await apiRequest("/auth/login", {
            method: "POST",
            body: JSON.stringify({
                email: document.getElementById("loginEmail").value,
                password: document.getElementById("loginPassword").value,
            }),
        });

        if (data.access_token) {
            token = data.access_token;
            localStorage.setItem("token", token);
            showChat();
        } else {
            alert("Login failed: " + (data.detail || "Unknown error"));
        }
    } catch (err) {
        alert(err.message);
    } finally {
        btn.disabled = false;
    }
}

async function signup() {
    try {
        await apiRequest("/auth/signup", {
            method: "POST",
            body: JSON.stringify({
                email: document.getElementById("signupEmail").value,
                password: document.getElementById("signupPassword").value,
                weight_kg: parseFloat(document.getElementById("signupWeight").value),
                height_cm: parseFloat(document.getElementById("signupHeight").value),
                age: parseInt(document.getElementById("signupAge").value),
                gender: document.getElementById("signupGender").value,
            }),
        });
        alert("Account created 🎉 Please login");
    } catch (err) {
        alert("Signup failed. Ensure all fields are filled correctly.");
    }
}

function logout() {
    localStorage.removeItem("token");
    token = null;
    document.getElementById("chat-section").classList.add("hidden");
    document.getElementById("auth-section").classList.remove("hidden");
    document.getElementById("chatBox").innerHTML = ""; 
}

function addMessage(sender, text) {
    const chatBox = document.getElementById("chatBox");
    const messageDiv = document.createElement("div");
    messageDiv.className = `chat-message ${sender === "user" ? "user-msg" : "bot-msg"}`;
    messageDiv.innerText = text;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTo({ top: chatBox.scrollHeight, behavior: 'smooth' });
}

async function sendMessage() {
    const input = document.getElementById("chatMessage");
    const msg = input.value.trim();
    if (!msg) return;

    input.value = "";
    addMessage("user", msg);

    const typingIndicator = document.createElement("div");
    typingIndicator.id = "typing";
    typingIndicator.className = "chat-message bot-msg italic";
    typingIndicator.innerText = "Physiq AI is thinking...";
    document.getElementById("chatBox").appendChild(typingIndicator);
    document.getElementById("chatBox").scrollTo({ top: document.getElementById("chatBox").scrollHeight, behavior: 'smooth' });

    try {
        const data = await apiRequest("/chat", {
            method: "POST",
            body: JSON.stringify({ message: msg }),
        });

        typingIndicator.remove();

        if (data.response) {
            addMessage("bot", data.response);
        } else {
            addMessage("bot", "⚠️ No response from server");
        }
    } catch (err) {
        if(document.getElementById("typing")) document.getElementById("typing").remove();
        addMessage("bot", "❌ Error connecting to server.");
    }
}
