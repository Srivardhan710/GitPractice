"""
DevPulse - Interactive Developer Hub & Web Dashboard
Single-file Flask Application containing back-end endpoints and inline dynamic UI.

Usage:
    python app.py
    Open http://127.0.0.1:5000 in your web browser.
"""

from flask import Flask, jsonify, request, render_template_string
import time
import random
from datetime import datetime

app = Flask(__name__)

# Start time for calculating server uptime
START_TIME = time.time()

# In-memory storage for sample tasks
TASKS_DB = [
    {"id": 1, "title": "Setup Flask Backend Architecture", "status": "completed", "category": "Backend"},
    {"id": 2, "title": "Design Glassmorphism Dashboard UI", "status": "completed", "category": "Frontend"},
    {"id": 3, "title": "Implement Real-time Analytics Visualizer", "status": "in-progress", "category": "Analytics"},
    {"id": 4, "title": "Configure Automated Deployment Pipeline", "status": "pending", "category": "DevOps"},
]

DEV_QUOTES = [
    {"quote": "Simplicity is prerequisite for reliability.", "author": "Edsger W. Dijkstra"},
    {"quote": "Make it work, make it right, make it fast.", "author": "Kent Beck"},
    {"quote": "First, solve the problem. Then, write the code.", "author": "John Johnson"},
    {"quote": "Code is like humor. When you have to explain it, it’s bad.", "author": "Cory House"},
    {"quote": "Experience is the name everyone gives to their mistakes.", "author": "Oscar Wilde"}
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DevPulse — Interactive Developer Hub</title>
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600&family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    
    <style>
        :root {
            --bg-primary: #090d16;
            --bg-secondary: #111827;
            --bg-card: rgba(17, 24, 39, 0.7);
            --bg-card-hover: rgba(31, 41, 55, 0.8);
            --border-color: rgba(255, 255, 255, 0.08);
            --accent-primary: #6366f1;
            --accent-glow: rgba(99, 102, 241, 0.35);
            --accent-secondary: #a855f7;
            --accent-cyan: #06b6d4;
            --accent-emerald: #10b981;
            --text-main: #f3f4f6;
            --text-muted: #9ca3af;
            --font-main: 'Inter', sans-serif;
            --font-code: 'Fira Code', monospace;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            background-color: var(--bg-primary);
            color: var(--text-main);
            font-family: var(--font-main);
            min-height: 100vh;
            overflow-x: hidden;
            line-height: 1.6;
        }

        /* Ambient Background Glow */
        .ambient-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            pointer-events: none;
            z-index: -1;
            overflow: hidden;
        }

        .glow-orb {
            position: absolute;
            border-radius: 50%;
            filter: blur(120px);
            opacity: 0.25;
            animation: floatOrb 18s ease-in-out infinite alternate;
        }

        .orb-1 {
            top: -10%;
            left: -10%;
            width: 50vw;
            height: 50vw;
            background: radial-gradient(circle, var(--accent-primary), transparent 70%);
        }

        .orb-2 {
            bottom: -20%;
            right: -10%;
            width: 60vw;
            height: 60vw;
            background: radial-gradient(circle, var(--accent-secondary), transparent 70%);
        }

        @keyframes floatOrb {
            0% { transform: translate(0, 0) scale(1); }
            50% { transform: translate(40px, 30px) scale(1.08); }
            100% { transform: translate(-20px, 50px) scale(0.95); }
        }

        /* Container Layout */
        .app-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem 1.5rem;
        }

        /* Header / Navbar */
        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 1.5rem;
            background: var(--bg-card);
            backdrop-filter: blur(16px);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            margin-bottom: 2.5rem;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }

        .logo-group {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .logo-icon {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            font-size: 1.25rem;
            color: #fff;
            box-shadow: 0 0 20px var(--accent-glow);
        }

        .logo-text {
            font-size: 1.35rem;
            font-weight: 700;
            letter-spacing: -0.02em;
            background: linear-gradient(to right, #fff, #9ca3af);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .server-status {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.875rem;
            color: var(--text-muted);
            background: rgba(255, 255, 255, 0.04);
            padding: 0.4rem 0.9rem;
            border-radius: 20px;
            border: 1px solid var(--border-color);
        }

        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: var(--accent-emerald);
            box-shadow: 0 0 10px var(--accent-emerald);
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.5; transform: scale(0.85); }
        }

        /* Hero Section */
        .hero-section {
            text-align: center;
            padding: 2.5rem 1rem;
            margin-bottom: 3rem;
        }

        .hero-badge {
            display: inline-block;
            padding: 0.35rem 1rem;
            border-radius: 30px;
            background: rgba(99, 102, 241, 0.12);
            border: 1px solid rgba(99, 102, 241, 0.3);
            color: #818cf8;
            font-size: 0.85rem;
            font-weight: 600;
            margin-bottom: 1.25rem;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }

        .hero-title {
            font-size: 3rem;
            font-weight: 800;
            line-height: 1.15;
            margin-bottom: 1.25rem;
            letter-spacing: -0.03em;
        }

        .gradient-text {
            background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #06b6d4 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .hero-subtitle {
            font-size: 1.15rem;
            color: var(--text-muted);
            max-width: 650px;
            margin: 0 auto 2rem auto;
            font-weight: 400;
        }

        /* Metric Cards Grid */
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 1.25rem;
            margin-bottom: 2.5rem;
        }

        .metric-card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 1.5rem;
            backdrop-filter: blur(12px);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .metric-card:hover {
            transform: translateY(-4px);
            border-color: rgba(99, 102, 241, 0.4);
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4);
        }

        .metric-label {
            font-size: 0.875rem;
            color: var(--text-muted);
            margin-bottom: 0.5rem;
            font-weight: 500;
        }

        .metric-value {
            font-size: 2rem;
            font-weight: 700;
            color: #fff;
            letter-spacing: -0.02em;
        }

        .metric-sub {
            font-size: 0.8rem;
            color: var(--accent-emerald);
            margin-top: 0.35rem;
            display: flex;
            align-items: center;
            gap: 0.25rem;
        }

        /* Section Layout */
        .dashboard-grid {
            display: grid;
            grid-template-columns: 7fr 5fr;
            gap: 1.5rem;
            margin-bottom: 2.5rem;
        }

        @media (max-width: 900px) {
            .dashboard-grid {
                grid-template-columns: 1fr;
            }
            .hero-title {
                font-size: 2.25rem;
            }
        }

        .card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 1.75rem;
            backdrop-filter: blur(14px);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
        }

        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid var(--border-color);
        }

        .card-title {
            font-size: 1.25rem;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 0.6rem;
        }

        .card-icon {
            color: var(--accent-primary);
        }

        /* Task Manager Component */
        .task-input-group {
            display: flex;
            gap: 0.75rem;
            margin-bottom: 1.25rem;
        }

        .input-field {
            flex: 1;
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 0.75rem 1rem;
            color: #fff;
            font-family: var(--font-main);
            font-size: 0.95rem;
            outline: none;
            transition: border-color 0.2s;
        }

        .input-field:focus {
            border-color: var(--accent-primary);
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
        }

        .btn {
            background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
            color: #fff;
            border: none;
            border-radius: 12px;
            padding: 0.75rem 1.3rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            font-size: 0.9rem;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
        }

        .btn:hover {
            opacity: 0.92;
            transform: translateY(-1px);
            box-shadow: 0 4px 15px var(--accent-glow);
        }

        .task-list {
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
            max-height: 320px;
            overflow-y: auto;
            padding-right: 0.25rem;
        }

        .task-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 0.85rem 1rem;
            transition: all 0.2s;
        }

        .task-item:hover {
            background: rgba(255, 255, 255, 0.06);
            border-color: rgba(255, 255, 255, 0.15);
        }

        .task-info {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .badge {
            font-size: 0.75rem;
            padding: 0.2rem 0.6rem;
            border-radius: 8px;
            font-weight: 600;
            text-transform: uppercase;
        }

        .badge-backend { background: rgba(99, 102, 241, 0.2); color: #818cf8; }
        .badge-frontend { background: rgba(168, 85, 247, 0.2); color: #c084fc; }
        .badge-analytics { background: rgba(6, 182, 212, 0.2); color: #22d3ee; }
        .badge-devops { background: rgba(245, 158, 11, 0.2); color: #fbbf24; }

        .btn-delete {
            background: transparent;
            border: none;
            color: #ef4444;
            cursor: pointer;
            padding: 0.3rem 0.5rem;
            border-radius: 6px;
            opacity: 0.7;
            transition: opacity 0.2s;
        }

        .btn-delete:hover {
            opacity: 1;
            background: rgba(239, 68, 68, 0.15);
        }

        /* Realtime Chart Simulation Canvas */
        .chart-container {
            position: relative;
            width: 100%;
            height: 220px;
            margin-top: 1rem;
        }

        canvas {
            width: 100%;
            height: 100%;
            border-radius: 12px;
        }

        /* Code Playground Section */
        .code-playground {
            font-family: var(--font-code);
            background: #050811;
            border: 1px solid var(--border-color);
            border-radius: 14px;
            padding: 1.25rem;
            position: relative;
        }

        .code-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.75rem;
            color: var(--text-muted);
            font-size: 0.8rem;
        }

        .code-dots {
            display: flex;
            gap: 6px;
        }

        .dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
        }

        .dot-red { background: #ef4444; }
        .dot-yellow { background: #f59e0b; }
        .dot-green { background: #10b981; }

        .code-content {
            color: #a7f3d0;
            font-size: 0.9rem;
            line-height: 1.5;
            white-space: pre-wrap;
        }

        /* Quote Banner */
        .quote-box {
            margin-top: 2rem;
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(168, 85, 247, 0.1));
            border: 1px solid rgba(99, 102, 241, 0.25);
            border-radius: 16px;
            padding: 1.5rem;
            text-align: center;
            position: relative;
        }

        .quote-text {
            font-style: italic;
            font-size: 1.1rem;
            color: #e0e7ff;
            margin-bottom: 0.5rem;
        }

        .quote-author {
            font-size: 0.85rem;
            color: var(--accent-cyan);
            font-weight: 600;
        }

        footer {
            text-align: center;
            margin-top: 4rem;
            padding: 2rem 0;
            color: var(--text-muted);
            font-size: 0.875rem;
            border-top: 1px solid var(--border-color);
        }
    </style>
</head>
<body>
    <div class="ambient-bg">
        <div class="glow-orb orb-1"></div>
        <div class="glow-orb orb-2"></div>
    </div>

    <div class="app-container">
        <!-- Navigation Header -->
        <header>
            <div class="logo-group">
                <div class="logo-icon">⚡</div>
                <div class="logo-text">DevPulse</div>
            </div>
            <div class="server-status">
                <div class="status-dot"></div>
                <span>Server: <strong id="server-status-text">Online</strong></span>
            </div>
        </header>

        <!-- Hero Section -->
        <section class="hero-section">
            <span class="hero-badge">Single-File Flask Application</span>
            <h1 class="hero-title">Real-Time Developer <br><span class="gradient-text">Innovation Dashboard</span></h1>
            <p class="hero-subtitle">
                A modern, high-performance web dashboard running entirely from a single <code>app.py</code> script. Designed with glassmorphism aesthetics & interactive APIs.
            </p>
        </section>

        <!-- Metrics Grid -->
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-label">Server Uptime</div>
                <div class="metric-value" id="uptime-val">0s</div>
                <div class="metric-sub">⚡ Active Process</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Active Tasks</div>
                <div class="metric-value" id="tasks-count-val">4</div>
                <div class="metric-sub">▲ 100% Synced</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Simulated Latency</div>
                <div class="metric-value" id="latency-val">12 ms</div>
                <div class="metric-sub">● Optimal Response</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">System Memory</div>
                <div class="metric-value" id="memory-val">42.8 %</div>
                <div class="metric-sub">✓ Stable State</div>
            </div>
        </div>

        <!-- Main Dashboard Content Grid -->
        <div class="dashboard-grid">
            <!-- Left Column: Task Manager -->
            <div class="card">
                <div class="card-header">
                    <div class="card-title">
                        <span class="card-icon">📌</span> Task & Sprint Manager
                    </div>
                    <span style="font-size: 0.85rem; color: var(--text-muted);" id="task-filter-info">Live REST Sync</span>
                </div>

                <form class="task-input-group" id="task-form">
                    <input type="text" class="input-field" id="task-input" placeholder="Add a new sprint task..." required>
                    <button type="submit" class="btn">+ Add Task</button>
                </form>

                <ul class="task-list" id="task-list-container">
                    <!-- Dynamic tasks will be inserted here -->
                </ul>
            </div>

            <!-- Right Column: Realtime Performance Visualizer -->
            <div class="card">
                <div class="card-header">
                    <div class="card-title">
                        <span class="card-icon">📈</span> Live Metrics Stream
                    </div>
                    <button class="btn" style="padding: 0.35rem 0.75rem; font-size: 0.8rem;" id="refresh-stats-btn">Refresh</button>
                </div>

                <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1rem;">
                    Dynamic canvas renderer fetching live simulated backend telemetry every 2 seconds.
                </p>

                <div class="chart-container">
                    <canvas id="metricsChart"></canvas>
                </div>
            </div>
        </div>

        <!-- Code Snippet & Interactive API Section -->
        <div class="dashboard-grid">
            <div class="card">
                <div class="card-header">
                    <div class="card-title">
                        <span class="card-icon">💻</span> App Architecture Preview
                    </div>
                </div>
                <div class="code-playground">
                    <div class="code-header">
                        <div class="code-dots">
                            <span class="dot dot-red"></span>
                            <span class="dot dot-yellow"></span>
                            <span class="dot dot-green"></span>
                        </div>
                        <span>app.py (Flask Core)</span>
                    </div>
                    <div class="code-content">from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/api/stats")
def stats():
    return jsonify({"uptime": time.time() - START_TIME})

if __name__ == "__main__":
    app.run(debug=True)</div>
                </div>
            </div>

            <!-- Developer Quote Card -->
            <div class="card" style="display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div class="card-header">
                        <div class="card-title">
                            <span class="card-icon">💡</span> Daily Dev Inspiration
                        </div>
                        <button class="btn" style="padding: 0.35rem 0.75rem; font-size: 0.8rem; background: rgba(255,255,255,0.1);" id="next-quote-btn">New Quote</button>
                    </div>
                    <div class="quote-box">
                        <div class="quote-text" id="quote-text">"Simplicity is prerequisite for reliability."</div>
                        <div class="quote-author" id="quote-author">— Edsger W. Dijkstra</div>
                    </div>
                </div>
                <div style="margin-top: 1.5rem; text-align: center;">
                    <span style="font-size: 0.85rem; color: var(--text-muted);">
                        Built with HTML5, CSS3, Vanilla JS, and Python Flask.
                    </span>
                </div>
            </div>
        </div>

        <!-- Footer -->
        <footer>
            <p>© 2026 DevPulse • Created in single-file <code>app.py</code></p>
        </footer>
    </div>

    <!-- Interactive Client Scripts -->
    <script>
        // Fetch Tasks from API
        async function fetchTasks() {
            try {
                const res = await fetch('/api/tasks');
                const tasks = await res.json();
                renderTasks(tasks);
            } catch (err) {
                console.error("Failed to load tasks", err);
            }
        }

        function renderTasks(tasks) {
            const container = document.getElementById('task-list-container');
            const countVal = document.getElementById('tasks-count-val');
            countVal.innerText = tasks.length;
            container.innerHTML = '';

            if (tasks.length === 0) {
                container.innerHTML = `<li style="text-align:center; color: var(--text-muted); padding: 1.5rem;">No active tasks. Add one above!</li>`;
                return;
            }

            tasks.forEach(task => {
                const li = document.createElement('li');
                li.className = 'task-item';
                
                const catClass = 'badge-' + (task.category || 'backend').toLowerCase();
                
                li.innerHTML = `
                    <div class="task-info">
                        <span class="badge ${catClass}">${task.category || 'Dev'}</span>
                        <span style="font-size: 0.95rem; font-weight: 500;">${escapeHtml(task.title)}</span>
                    </div>
                    <button class="btn-delete" onclick="deleteTask(${task.id})" title="Delete Task">✕</button>
                `;
                container.appendChild(li);
            });
        }

        // Add New Task
        document.getElementById('task-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const input = document.getElementById('task-input');
            const title = input.value.trim();
            if (!title) return;

            const categories = ['Backend', 'Frontend', 'Analytics', 'DevOps'];
            const randomCat = categories[Math.floor(Math.random() * categories.length)];

            try {
                const res = await fetch('/api/tasks', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ title, category: randomCat })
                });
                if (res.ok) {
                    input.value = '';
                    fetchTasks();
                }
            } catch (err) {
                console.error("Failed to add task", err);
            }
        });

        // Delete Task
        async function deleteTask(id) {
            try {
                const res = await fetch(`/api/tasks?id=${id}`, { method: 'DELETE' });
                if (res.ok) {
                    fetchTasks();
                }
            } catch (err) {
                console.error("Failed to delete task", err);
            }
        }

        // Fetch Live Stats Telemetry
        async function fetchStats() {
            try {
                const res = await fetch('/api/stats');
                const data = await res.json();
                
                document.getElementById('uptime-val').innerText = Math.floor(data.uptime) + 's';
                document.getElementById('latency-val').innerText = data.latency + ' ms';
                document.getElementById('memory-val').innerText = data.memory_usage + ' %';
                
                pushChartData(data.latency);
            } catch (err) {
                console.error("Failed to fetch stats", err);
            }
        }

        // Fetch Quote
        async function fetchQuote() {
            try {
                const res = await fetch('/api/quote');
                const data = await res.json();
                document.getElementById('quote-text').innerText = `"${data.quote}"`;
                document.getElementById('quote-author').innerText = `— ${data.author}`;
            } catch (err) {
                console.error("Failed to fetch quote", err);
            }
        }

        document.getElementById('next-quote-btn').addEventListener('click', fetchQuote);
        document.getElementById('refresh-stats-btn').addEventListener('click', fetchStats);

        // Helper to prevent XSS
        function escapeHtml(text) {
            return text.replace(/[&<>"']/g, (m) => ({
                '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;'
            })[m]);
        }

        // Realtime Canvas Chart Implementation
        const canvas = document.getElementById('metricsChart');
        const ctx = canvas.getContext('2d');
        let chartData = [15, 18, 12, 22, 19, 25, 14, 20, 16, 22, 18, 12];

        function resizeCanvas() {
            canvas.width = canvas.parentElement.clientWidth;
            canvas.height = canvas.parentElement.clientHeight;
            drawChart();
        }

        function pushChartData(val) {
            chartData.push(val);
            if (chartData.length > 20) chartData.shift();
            drawChart();
        }

        function drawChart() {
            if (!ctx) return;
            const w = canvas.width;
            const h = canvas.height;

            ctx.clearRect(0, 0, w, h);

            // Draw Background Grid Lines
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
            ctx.lineWidth = 1;
            for (let y = 0; y < h; y += 40) {
                ctx.beginPath();
                ctx.moveTo(0, y);
                ctx.lineTo(w, y);
                ctx.stroke();
            }

            // Draw Line Chart
            const step = w / (chartData.length - 1);
            const maxVal = Math.max(...chartData, 50);
            const minVal = 0;

            ctx.beginPath();
            chartData.forEach((val, i) => {
                const x = i * step;
                const y = h - ((val - minVal) / (maxVal - minVal)) * (h - 40) - 20;
                if (i === 0) ctx.moveTo(x, y);
                else ctx.lineTo(x, y);
            });

            // Gradient Fill
            const gradient = ctx.createLinearGradient(0, 0, 0, h);
            gradient.addColorStop(0, 'rgba(99, 102, 241, 0.4)');
            gradient.addColorStop(1, 'rgba(99, 102, 241, 0.0)');

            ctx.lineTo(w, h);
            ctx.lineTo(0, h);
            ctx.closePath();
            ctx.fillStyle = gradient;
            ctx.fill();

            // Draw Line Stroke
            ctx.beginPath();
            chartData.forEach((val, i) => {
                const x = i * step;
                const y = h - ((val - minVal) / (maxVal - minVal)) * (h - 40) - 20;
                if (i === 0) ctx.moveTo(x, y);
                else ctx.lineTo(x, y);
            });
            ctx.strokeStyle = '#6366f1';
            ctx.lineWidth = 3;
            ctx.stroke();

            // Draw Data Points
            chartData.forEach((val, i) => {
                const x = i * step;
                const y = h - ((val - minVal) / (maxVal - minVal)) * (h - 40) - 20;
                ctx.beginPath();
                ctx.arc(x, y, 4, 0, Math.PI * 2);
                ctx.fillStyle = '#a855f7';
                ctx.fill();
            });
        }

        window.addEventListener('resize', resizeCanvas);

        // Initial Initialization
        window.addEventListener('DOMContentLoaded', () => {
            resizeCanvas();
            fetchTasks();
            fetchStats();
            // Auto refresh telemetry stats every 2 seconds
            setInterval(fetchStats, 2000);
        });
    </script>
</body>
</html>
"""

# ==================== BACKEND REST ROUTES ====================

@app.route("/")
def home():
    """Renders the single-file UI dashboard."""
    return render_template_string(HTML_TEMPLATE)

@app.route("/api/stats", methods=["GET"])
def get_stats():
    """Returns telemetry and metric data."""
    uptime = time.time() - START_TIME
    return jsonify({
        "status": "online",
        "uptime": round(uptime, 1),
        "latency": random.randint(10, 35),
        "memory_usage": round(random.uniform(38.0, 48.5), 1),
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })

@app.route("/api/tasks", methods=["GET", "POST", "DELETE"])
def handle_tasks():
    """REST API endpoint for managing task items in memory."""
    global TASKS_DB

    if request.method == "GET":
        return jsonify(TASKS_DB)

    elif request.method == "POST":
        data = request.get_json() or {}
        title = data.get("title", "").strip()
        category = data.get("category", "Dev")
        if not title:
            return jsonify({"error": "Task title required"}), 400

        new_task = {
            "id": len(TASKS_DB) + 1 if not TASKS_DB else max(t["id"] for t in TASKS_DB) + 1,
            "title": title,
            "status": "pending",
            "category": category
        }
        TASKS_DB.append(new_task)
        return jsonify(new_task), 201

    elif request.method == "DELETE":
        task_id = request.args.get("id", type=int)
        if not task_id:
            return jsonify({"error": "Task ID required"}), 400
        
        TASKS_DB = [t for t in TASKS_DB if t["id"] != task_id]
        return jsonify({"success": True})

@app.route("/api/quote", methods=["GET"])
def get_quote():
    """Returns a random developer quote."""
    return jsonify(random.choice(DEV_QUOTES))

if __name__ == "__main__":
    print("🚀 Starting DevPulse Dashboard Server on http://127.0.0.1:5000 ...")
    app.run(debug=True, port=5000)
