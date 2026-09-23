# ⚡ DevPulse — Interactive Developer Hub & Web Dashboard

DevPulse is a modern, responsive, single-file web application built with **Flask (Python)**, featuring a glassmorphism design system, real-time metrics telemetry visualizer, interactive task manager, and REST API endpoints — all contained within a single `app.py` script.

---

## ✨ Features

- 🎨 **Glassmorphism UI & Dark Aesthetics**: Built with custom HSL/RGB CSS variables, smooth ambient glowing background orbs, Google Fonts (`Inter` & `Fira Code`), and micro-animations.
- 📌 **Interactive Task & Sprint Manager**: Full in-memory REST API integration (`GET`, `POST`, `DELETE`) allowing users to add and manage tasks live without full page refreshes.
- 📈 **Real-Time Telemetry Canvas Visualizer**: An HTML5 Canvas chart that streams simulated server metrics (uptime, latency, memory usage) refreshed dynamically via polling.
- 💡 **Daily Dev Inspiration**: Interactive quotes generator powered by a dedicated Flask API route.
- 🛠️ **Single-File Architecture**: Complete web app (backend logic, templates, CSS styling, and client-side JavaScript) self-contained in `app.py`.

---

## 🚀 Quick Start

### Prerequisites

Ensure you have **Python 3.7+** installed.

### 1. Install Dependencies

Install **Flask** via `pip`:

```bash
pip install flask
```

### 2. Run the Application

Execute the single file `app.py`:

```bash
python app.py
```

### 3. Open in Browser

Navigate to:
[http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 📡 API Reference

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/` | `GET` | Renders the primary dashboard UI webpage |
| `/api/stats` | `GET` | Returns JSON telemetry data (uptime, latency, memory usage) |
| `/api/tasks` | `GET` | Retrieves all current tasks |
| `/api/tasks` | `POST` | Creates a new task (body: `{"title": "Task name", "category": "Dev"}`) |
| `/api/tasks` | `DELETE` | Deletes a task by ID (query parameter `?id=<id>`) |
| `/api/quote` | `GET` | Returns a random developer quote |

---

## 📁 File Structure

```text
GitPractice/
├── app.py       # Single-file Flask app containing UI template, CSS, JS & REST backend
└── README.md    # Project documentation and setup guide
```
