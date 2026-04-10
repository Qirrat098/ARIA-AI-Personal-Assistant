const API_BASE = "http://localhost:8000/api";

async function fetchJson(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: { "Content-Type": "application/json", ...options.headers },
            ...options,
        });
        if (!response.ok) throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        return response.json();
    } catch (error) {
        if (error instanceof TypeError) {
            throw new Error("Backend server not running on localhost:8000");
        }
        throw error;
    }
}

async function sendChat(message) {
    const data = await fetchJson(`${API_BASE}/chat`, {
        method: "POST",
        body: JSON.stringify({ message }),
    });
    return data.response;
}

async function addTask(title, description) {
    return fetchJson(`${API_BASE}/tasks`, {
        method: "POST",
        body: JSON.stringify({ title, description }),
    });
}

async function getTasks() {
    return fetchJson(`${API_BASE}/tasks`);
}

async function addNote(title, content) {
    return fetchJson(`${API_BASE}/notes`, {
        method: "POST",
        body: JSON.stringify({ title, content }),
    });
}

async function getNotes() {
    return fetchJson(`${API_BASE}/notes`);
}

async function checkStatus() {
    try {
        const data = await fetchJson(`${API_BASE}/status`);
        document.getElementById("status").textContent = "✓ Connected";
        document.getElementById("status").style.color = "green";
        return true;
    } catch {
        document.getElementById("status").textContent = "✗ Disconnected";
        document.getElementById("status").style.color = "red";
        return false;
    }
}

document.getElementById("chat-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const input = document.getElementById("chat-input");
    const message = input.value.trim();
    if (!message) return;

    const log = document.getElementById("chat-log");
    log.innerHTML += `<div class="message user-message"><div class="content">${escapeHtml(message)}</div></div>`;

    try {
        const response = await sendChat(message);
        log.innerHTML += `<div class="message bot-message"><div class="content">${escapeHtml(response)}</div></div>`;
    } catch (e) {
        log.innerHTML += `<div class="message error-message"><div class="content">Error: ${escapeHtml(e.message)}</div></div>`;
    }

    input.value = "";
    log.scrollTop = log.scrollHeight;
});

document.getElementById("task-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const input = document.getElementById("task-input");
    const title = input.value.trim();
    if (!title) return;

    try {
        await addTask(title);
        await refreshTasks();
        input.value = "";
    } catch (e) {
        alert(`Error adding task: ${e.message}`);
    }
});

document.getElementById("note-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const titleInput = document.getElementById("note-title");
    const contentInput = document.getElementById("note-content");
    const title = titleInput.value.trim();
    const content = contentInput.value.trim();
    if (!title || !content) return;

    try {
        await addNote(title, content);
        await refreshNotes();
        titleInput.value = "";
        contentInput.value = "";
    } catch (e) {
        alert(`Error adding note: ${e.message}`);
    }
});

async function refreshTasks() {
    try {
        const tasks = await getTasks();
        const list = document.getElementById("task-list");
        list.innerHTML = tasks.map(t => `<li><strong>${escapeHtml(t.title)}</strong> — ${escapeHtml(t.description || "")}</li>`).join("");
    } catch (e) {
        console.error("Error refreshing tasks:", e);
    }
}

async function refreshNotes() {
    try {
        const notes = await getNotes();
        const list = document.getElementById("note-list");
        list.innerHTML = notes.map(n => `<li><strong>${escapeHtml(n.title)}</strong><br>${escapeHtml(n.content)}</li>`).join("");
    } catch (e) {
        console.error("Error refreshing notes:", e);
    }
}

function escapeHtml(text) {
    const map = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;" };
    return text.replace(/[&<>"']/g, m => map[m]);
}

window.addEventListener("load", async () => {
    await checkStatus();
    await refreshTasks();
    await refreshNotes();
    setInterval(checkStatus, 5000);
});
