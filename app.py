
from flask import Flask, request, redirect, url_for, render_template_string, make_response
import sqlite3
import csv
import io
from pathlib import Path
from datetime import datetime

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "civicpulse.db"

# Change these example names to your team members' names if needed.
WORKERS = [
    "Unassigned",
    "Rahul",
    "Priya",
    "Amit",
    "Sneha"
]


def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_db() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS service_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                location TEXT NOT NULL,
                description TEXT NOT NULL,
                priority TEXT NOT NULL DEFAULT 'Medium',
                status TEXT NOT NULL DEFAULT 'Pending',
                created_at TEXT NOT NULL
            )
        """)

        # Add the worker column to an existing database if necessary.
        columns = [
            row["name"]
            for row in connection.execute(
                "PRAGMA table_info(service_requests)"
            ).fetchall()
        ]

        if "assigned_worker" not in columns:
            connection.execute("""
                ALTER TABLE service_requests
                ADD COLUMN assigned_worker TEXT NOT NULL
                DEFAULT 'Unassigned'
            """)


HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CivicPulse | Service Operations</title>

    <style>
        * { box-sizing: border-box; }

        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #f3f6fb;
            color: #1e293b;
        }

        header {
            background: #123b65;
            color: white;
            padding: 24px 7%;
        }

        header h1 { margin: 0 0 8px; }
        header p { margin: 0; color: #dbeafe; }

        main {
            max-width: 1200px;
            margin: 30px auto;
            padding: 0 20px;
        }

        .cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
            gap: 16px;
        }

        .card, .panel {
            background: white;
            padding: 22px;
            border-radius: 12px;
            box-shadow: 0 3px 12px #0000000c;
        }

        .card { border-left: 5px solid #2878c8; }
        .card p { color: #64748b; margin-top: 0; }
        .number { font-size: 30px; font-weight: bold; }

        .panel { margin-top: 25px; }
        .panel h2 { margin-top: 0; }
        .muted { color: #64748b; }

        .form-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 16px;
        }

        .field {
            display: flex;
            flex-direction: column;
            gap: 7px;
        }

        .full { grid-column: 1 / -1; }

        input, select, textarea {
            width: 100%;
            padding: 11px;
            border: 1px solid #cbd5e1;
            border-radius: 7px;
            font: inherit;
        }

        textarea { min-height: 90px; }

        button {
            background: #1768ac;
            color: white;
            border: 0;
            padding: 10px 14px;
            border-radius: 7px;
            cursor: pointer;
        }

        button:hover { background: #104e83; }

        .table-wrap { overflow-x: auto; }

        table {
            width: 100%;
            min-width: 900px;
            border-collapse: collapse;
        }

        th, td {
            padding: 12px 10px;
            text-align: left;
            border-bottom: 1px solid #e2e8f0;
            vertical-align: top;
        }

        th { background: #f8fafc; }

        .status {
            display: inline-block;
            padding: 5px 9px;
            border-radius: 20px;
            font-size: 12px;
            background: #fef3c7;
            color: #92400e;
        }

        .status-progress {
            background: #dbeafe;
            color: #1d4ed8;
        }

        .status-completed {
            background: #dcfce7;
            color: #166534;
        }

        .message {
            background: #dcfce7;
            color: #166534;
            padding: 12px;
            border-radius: 7px;
            margin-bottom: 18px;
        }

        .inline-form {
            display: flex;
            gap: 6px;
            align-items: center;
        }

        .inline-form select { min-width: 130px; }

        .worker-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
            gap: 14px;
        }

        .worker-card {
            background: #f8fafc;
            padding: 16px;
            border-radius: 9px;
            border: 1px solid #e2e8f0;
        }

        footer {
            text-align: center;
            padding: 25px;
            color: #64748b;
        }

        @media (max-width: 600px) {
            header { padding: 22px; }
            .full { grid-column: auto; }
        }
    </style>
</head>

<body>
<header>
    <h1>CivicPulse</h1>
    <p>Public Service Usage and Operations Management System</p>
</header>

<main>
    <h2>Operations Dashboard</h2>
    <p class="muted">Monitor service requests, team assignments and progress.</p>

    {% if message %}
        <div class="message">{{ message }}</div>
    {% endif %}

    <div class="cards">
        <div class="card">
            <p>Total Requests</p>
            <div class="number">{{ total }}</div>
        </div>
        <div class="card">
            <p>Pending</p>
            <div class="number">{{ pending }}</div>
        </div>
        <div class="card">
            <p>In Progress</p>
            <div class="number">{{ in_progress }}</div>
        </div>
        <div class="card">
            <p>Completed</p>
            <div class="number">{{ completed }}</div>
        </div>
    </div>

    <section class="panel">
        <h2>Register a Service Request</h2>

        <form action="{{ url_for('add_request') }}" method="POST"
              class="form-grid">

            <div class="field">
                <label for="title">Request title</label>
                <input id="title" name="title" maxlength="100"
                       placeholder="Streetlight not working" required>
            </div>

            <div class="field">
                <label for="category">Service category</label>
                <select id="category" name="category" required>
                    <option value="">Choose category</option>
                    <option>Streetlight</option>
                    <option>Waste Collection</option>
                    <option>Water Supply</option>
                    <option>Road Maintenance</option>
                    <option>Public Cleanliness</option>
                    <option>Other</option>
                </select>
            </div>

            <div class="field">
                <label for="location">Location</label>
                <input id="location" name="location" maxlength="150"
                       placeholder="Area or street" required>
            </div>

            <div class="field">
                <label for="priority">Priority</label>
                <select id="priority" name="priority" required>
                    <option>Low</option>
                    <option selected>Medium</option>
                    <option>High</option>
                </select>
            </div>

            <div class="field">
                <label for="worker">Assign worker</label>
                <select id="worker" name="assigned_worker" required>
                    {% for worker in workers %}
                        <option value="{{ worker }}">{{ worker }}</option>
                    {% endfor %}
                </select>
            </div>

            <div class="field full">
                <label for="description">Description</label>
                <textarea id="description" name="description"
                          maxlength="1000"
                          placeholder="Describe the problem..." required></textarea>
            </div>

            <div class="full">
                <button type="submit">Submit Service Request</button>
            </div>
        </form>
    </section>

    <section class="panel">
        <h2>Worker Workload</h2>
        <p class="muted">Number of requests assigned to each team member.</p>

        <div class="worker-grid">
            {% for worker in workers %}
                {% if worker != "Unassigned" %}
                    <div class="worker-card">
                        <strong>{{ worker }}</strong>
                        <p>
                            Total assigned:
                            <strong>{{ workload[worker]["total"] }}</strong>
                        </p>
                        <p>
                            Still open:
                            <strong>{{ workload[worker]["open"] }}</strong>
                        </p>
                    </div>
                {% endif %}
            {% endfor %}
        </div>

        <p class="muted">
            These are example team members. You can change their names
            in the WORKERS list in app.py.
        </p>
    </section>

    <section class="panel">
        <h2>All Service Requests</h2>
        <p class="muted">Search and filter requests without changing the saved records.</p>

        <form action="{{ url_for('home') }}" method="GET" class="form-grid" style="margin-bottom: 18px;">
            <div class="field">
                <label for="search">Search</label>
                <input id="search" name="q" value="{{ search_q }}"
                       placeholder="Title, location, description or ID">
            </div>
            <div class="field">
                <label for="filter_status">Status</label>
                <select id="filter_status" name="status">
                    <option value="">All statuses</option>
                    {% for status in statuses %}
                        <option value="{{ status }}" {% if filter_status == status %}selected{% endif %}>{{ status }}</option>
                    {% endfor %}
                </select>
            </div>
            <div class="field">
                <label for="filter_category">Category</label>
                <select id="filter_category" name="category">
                    <option value="">All categories</option>
                    {% for category in categories %}
                        <option value="{{ category }}" {% if filter_category == category %}selected{% endif %}>{{ category }}</option>
                    {% endfor %}
                </select>
            </div>
            <div class="field">
                <label for="filter_priority">Priority</label>
                <select id="filter_priority" name="priority">
                    <option value="">All priorities</option>
                    {% for priority in priorities %}
                        <option value="{{ priority }}" {% if filter_priority == priority %}selected{% endif %}>{{ priority }}</option>
                    {% endfor %}
                </select>
            </div>
            <div class="field">
                <label for="filter_worker">Assigned worker</label>
                <select id="filter_worker" name="worker">
                    <option value="">All workers</option>
                    {% for worker in workers %}
                        <option value="{{ worker }}" {% if filter_worker == worker %}selected{% endif %}>{{ worker }}</option>
                    {% endfor %}
                </select>
            </div>
            <div class="full" style="display:flex; gap:10px; flex-wrap:wrap; align-items:center;">
                <button type="submit">Apply Filters</button>
                <a href="{{ url_for('home') }}" style="padding:10px 4px;">Clear Filters</a>
                <a href="{{ url_for('export_csv', q=search_q, status=filter_status, category=filter_category, priority=filter_priority, worker=filter_worker) }}" style="padding:10px 4px;">Download CSV Report</a>
                <a href="{{ url_for('analytics') }}" style="padding:10px 4px;">View Analytics</a>
            </div>
        </form>
        <p class="muted">Showing {{ requests|length }} matching request(s).</p>

        {% if requests %}
        <div class="table-wrap">
            <table>
                <thead>
                    <tr>
                        <th>ID / Date</th>
                        <th>Request</th>
                        <th>Location</th>
                        <th>Priority</th>
                        <th>Assigned Worker</th>
                        <th>Status</th>
                        <th>Update</th>
                    </tr>
                </thead>
                <tbody>
                {% for item in requests %}
                    <tr>
                        <td>
                            CP-{{ "%03d"|format(item.id) }}
                            <br><small class="muted">{{ item.created_at }}</small>
                        </td>
                        <td>
                            <strong>{{ item.title }}</strong>
                            <br><small class="muted">{{ item.category }}</small>
                            <br>{{ item.description }}
                        </td>
                        <td>{{ item.location }}</td>
                        <td>{{ item.priority }}</td>
                        <td>{{ item.assigned_worker }}</td>
                        <td>
                            {% if item.status == "Completed" %}
                                <span class="status status-completed">{{ item.status }}</span>
                            {% elif item.status == "In Progress" %}
                                <span class="status status-progress">{{ item.status }}</span>
                            {% else %}
                                <span class="status">{{ item.status }}</span>
                            {% endif %}
                        </td>
                        <td>
                            <form class="inline-form"
                                  action="{{ url_for('update_request',
                                      request_id=item.id) }}"
                                  method="POST">
                                <select name="status" aria-label="Request status">
                                    {% for status in statuses %}
                                        <option value="{{ status }}"
                                            {% if item.status == status %}selected{% endif %}>
                                            {{ status }}
                                        </option>
                                    {% endfor %}
                                </select>

                                <select name="assigned_worker"
                                        aria-label="Assigned worker">
                                    {% for worker in workers %}
                                        <option value="{{ worker }}"
                                            {% if item.assigned_worker == worker %}selected{% endif %}>
                                            {{ worker }}
                                        </option>
                                    {% endfor %}
                                </select>
                                <button type="submit">Save</button>
                            </form>
                        </td>
                    </tr>
                {% endfor %}
                </tbody>
            </table>
        </div>
        {% else %}
            <p class="muted">No requests yet. Submit your first request above.</p>
        {% endif %}
    </section>
</main>

<footer>CivicPulse | Public Service Operations Project</footer>
</body>
</html>
"""


def get_filtered_requests(args):
    """Return requests matching the supplied search and filter arguments."""
    search_q = args.get("q", "").strip()
    filter_status = args.get("status", "").strip()
    filter_category = args.get("category", "").strip()
    filter_priority = args.get("priority", "").strip()
    filter_worker = args.get("worker", "").strip()

    conditions = []
    values = []

    if search_q:
        like_value = f"%{search_q}%"
        conditions.append("(title LIKE ? OR category LIKE ? OR location LIKE ? OR description LIKE ? OR CAST(id AS TEXT) LIKE ?)")
        values.extend([like_value] * 5)
    if filter_status in ["Pending", "In Progress", "Completed"]:
        conditions.append("status = ?")
        values.append(filter_status)
    if filter_category:
        conditions.append("category = ?")
        values.append(filter_category)
    if filter_priority in ["Low", "Medium", "High"]:
        conditions.append("priority = ?")
        values.append(filter_priority)
    if filter_worker in WORKERS:
        conditions.append("COALESCE(assigned_worker, 'Unassigned') = ?")
        values.append(filter_worker)

    sql = "SELECT * FROM service_requests"
    if conditions:
        sql += " WHERE " + " AND ".join(conditions)
    sql += " ORDER BY id DESC"

    with get_db() as connection:
        matching_requests = connection.execute(sql, values).fetchall()

    return matching_requests, search_q, filter_status, filter_category, filter_priority, filter_worker


@app.route("/")
def home():
    # Use all saved records for dashboard totals and worker workload so filters
    # do not change the overall project statistics.
    with get_db() as connection:
        all_requests = connection.execute(
            "SELECT * FROM service_requests ORDER BY id DESC"
        ).fetchall()
        category_rows = connection.execute(
            "SELECT DISTINCT category FROM service_requests ORDER BY category"
        ).fetchall()

    requests_list, search_q, filter_status, filter_category, filter_priority, filter_worker = get_filtered_requests(request.args)
    total = len(all_requests)
    pending = sum(r["status"] == "Pending" for r in all_requests)
    in_progress = sum(r["status"] == "In Progress" for r in all_requests)
    completed = sum(r["status"] == "Completed" for r in all_requests)

    workload = {
        worker: {"total": 0, "open": 0}
        for worker in WORKERS if worker != "Unassigned"
    }
    for item in all_requests:
        worker = item["assigned_worker"] or "Unassigned"
        if worker in workload:
            workload[worker]["total"] += 1
            if item["status"] != "Completed":
                workload[worker]["open"] += 1

    categories = sorted(set([row["category"] for row in category_rows] + [
        "Streetlight", "Waste Collection", "Water Supply", "Road Maintenance",
        "Public Cleanliness", "Other"
    ]))

    return render_template_string(
        HTML,
        requests=requests_list,
        total=total,
        pending=pending,
        in_progress=in_progress,
        completed=completed,
        workers=WORKERS,
        workload=workload,
        statuses=["Pending", "In Progress", "Completed"],
        categories=categories,
        priorities=["Low", "Medium", "High"],
        search_q=search_q,
        filter_status=filter_status,
        filter_category=filter_category,
        filter_priority=filter_priority,
        filter_worker=filter_worker,
        message=request.args.get("message", "")
    )


@app.route("/export-csv")
def export_csv():
    records, search_q, filter_status, filter_category, filter_priority, filter_worker = get_filtered_requests(request.args)
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Request ID", "Title", "Category", "Location", "Description", "Priority", "Status", "Assigned Worker", "Created At"])
    for item in records:
        writer.writerow([
            item["id"], item["title"], item["category"], item["location"],
            item["description"], item["priority"], item["status"],
            item["assigned_worker"] or "Unassigned", item["created_at"]
        ])

    response = make_response("\ufeff" + output.getvalue())
    response.headers["Content-Type"] = "text/csv; charset=utf-8"
    response.headers["Content-Disposition"] = "attachment; filename=civicpulse_service_requests.csv"
    return response


@app.route("/add", methods=["POST"])
def add_request():
    title = request.form.get("title", "").strip()
    category = request.form.get("category", "").strip()
    location = request.form.get("location", "").strip()
    description = request.form.get("description", "").strip()
    priority = request.form.get("priority", "Medium").strip()
    worker = request.form.get("assigned_worker", "Unassigned").strip()

    if not all([title, category, location, description]):
        return redirect(url_for("home", message="Please fill in all required fields."))

    if priority not in ["Low", "Medium", "High"]:
        priority = "Medium"

    if worker not in WORKERS:
        worker = "Unassigned"

    created_at = datetime.now().strftime("%d-%m-%Y %H:%M")

    with get_db() as connection:
        connection.execute("""
            INSERT INTO service_requests
            (title, category, location, description, priority,
             status, created_at, assigned_worker)
            VALUES (?, ?, ?, ?, ?, 'Pending', ?, ?)
        """, (
            title, category, location, description, priority,
            created_at, worker
        ))

    return redirect(url_for("home", message="Request submitted successfully!"))


@app.route("/update/<int:request_id>", methods=["POST"])
def update_request(request_id):
    status = request.form.get("status", "")
    worker = request.form.get("assigned_worker", "Unassigned")

    if status not in ["Pending", "In Progress", "Completed"]:
        return redirect(url_for("home", message="Invalid status."))

    if worker not in WORKERS:
        worker = "Unassigned"

    with get_db() as connection:
        connection.execute("""
            UPDATE service_requests
            SET status = ?, assigned_worker = ?
            WHERE id = ?
        """, (status, worker, request_id))

    return redirect(url_for(
        "home", message="Request and worker assignment updated!"
    ))


@app.route("/analytics")
def analytics():
    with get_db() as connection:
        records = connection.execute("""
            SELECT category, status, assigned_worker
            FROM service_requests
        """).fetchall()

    # Count requests by status
    status_counts = {
        "Pending": 0,
        "In Progress": 0,
        "Completed": 0
    }

    category_counts = {}
    worker_counts = {}

    for record in records:
        status = record["status"]

        if status in status_counts:
            status_counts[status] += 1

        category = record["category"]
        category_counts[category] = category_counts.get(category, 0) + 1

        worker = record["assigned_worker"] or "Unassigned"
        worker_counts[worker] = worker_counts.get(worker, 0) + 1

    total = len(records)
    completed = status_counts["Completed"]

    completion_rate = (
        round((completed / total) * 100, 1)
        if total else 0
    )

    # Create charts
    import plotly.graph_objects as go
    import plotly.io as pio

    status_chart = go.Figure(
        data=[go.Bar(
            x=list(status_counts.keys()),
            y=list(status_counts.values()),
            text=list(status_counts.values()),
            textposition="auto"
        )]
    )
    status_chart.update_layout(
        title="Requests by Status",
        xaxis_title="Status",
        yaxis_title="Number of Requests",
        template="plotly_white"
    )

    category_chart = go.Figure(
        data=[go.Pie(
            labels=list(category_counts.keys()),
            values=list(category_counts.values()),
            hole=0.35
        )]
    )
    category_chart.update_layout(
        title="Requests by Service Category",
        template="plotly_white"
    )

    worker_chart = go.Figure(
        data=[go.Bar(
            x=list(worker_counts.keys()),
            y=list(worker_counts.values()),
            text=list(worker_counts.values()),
            textposition="auto"
        )]
    )
    worker_chart.update_layout(
        title="Requests Assigned to Each Worker",
        xaxis_title="Worker",
        yaxis_title="Total Assigned",
        template="plotly_white"
    )

    status_html = pio.to_html(
        status_chart, full_html=False, include_plotlyjs="cdn"
    )
    category_html = pio.to_html(
        category_chart, full_html=False, include_plotlyjs=False
    )
    worker_html = pio.to_html(
        worker_chart, full_html=False, include_plotlyjs=False
    )

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>CivicPulse Analytics</title>
        <style>
            * { box-sizing: border-box; }
            body {
                font-family: Arial, sans-serif;
                background: #f1f5f9;
                color: #1e293b;
                margin: 0;
                line-height: 1.55;
            }
            header {
                background: linear-gradient(120deg, #102f50, #1768ac);
                color: white;
                padding: 30px 7%;
                box-shadow: 0 4px 14px #0f172a18;
            }
            header h1 { margin: 0 0 8px; }
            header p { margin: 0; color: #dbeafe; }
            main {
                max-width: 1320px;
                margin: 30px auto;
                padding: 0 24px;
            }
            h2 { color: #123b65; }
            .cards {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                gap: 16px;
            }
            .card, .chart {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 16px;
                padding: 22px;
                margin-bottom: 20px;
                box-shadow: 0 5px 18px #0f172a0a;
            }
            .number {
                color: #123b65;
                font-size: 34px;
                font-weight: bold;
            }
            .muted { color: #64748b; }
            a {
                display: inline-block;
                margin: 10px 0 22px;
                color: #1768ac;
            }
            a:focus-visible {
                outline: 3px solid #60a5fa;
                outline-offset: 3px;
            }
            @media (max-width: 600px) {
                main { padding: 0 14px; margin-top: 20px; }
                .card, .chart { padding: 18px; }
                .number { font-size: 28px; }
            }
        </style>
    </head>
    <body>
        <header>
            <h1>CivicPulse Analytics</h1>
            <p>Service Operations and Performance Reports</p>
        </header>
        <main>
            <a href="/">← Back to Operations Dashboard</a>

            <h2>Analytics Overview</h2>
            <p class="muted">
                These statistics use the requests currently saved in your database.
            </p>

            <div class="cards">
                <div class="card">
                    <p>Total Requests</p>
                    <div class="number">{{ total }}</div>
                </div>
                <div class="card">
                    <p>Pending</p>
                    <div class="number">{{ pending }}</div>
                </div>
                <div class="card">
                    <p>In Progress</p>
                    <div class="number">{{ in_progress }}</div>
                </div>
                <div class="card">
                    <p>Completion Rate</p>
                    <div class="number">{{ rate }}%</div>
                </div>
            </div>

            <div class="chart">{{ status_chart|safe }}</div>
            <div class="chart">{{ category_chart|safe }}</div>
            <div class="chart">{{ worker_chart|safe }}</div>
        </main>
    </body>
    </html>
    """,
        total=total,
        pending=status_counts["Pending"],
        in_progress=status_counts["In Progress"],
        rate=completion_rate,
        status_chart=status_html,
        category_chart=category_html,
        worker_chart=worker_html
    )



# Initialize the database when the app is imported by Render/Gunicorn
init_db()

if __name__ == "__main__":
    print("CivicPulse database is ready.")
    print("Open http://127.0.0.1:5000 in your browser.")
    app.run(debug=False)

