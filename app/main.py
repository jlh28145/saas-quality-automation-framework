"""
Simple SaaS-style Flask application for testing demonstration.
Supports UI and API testing with deterministic behaviors.
"""

import json
import os
from datetime import datetime
from functools import wraps
from pathlib import Path

from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "test-secret-key-do-not-use-in-production"

# Directories
DATA_DIR = Path(__file__).parent.parent / "data"
REPORTS_DIR = Path(__file__).parent.parent / "reports"
LOGS_DIR = REPORTS_DIR / "logs"

LOGS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Test data
VALID_USERS = {
    "testuser@example.com": {"password": "password123", "name": "Test User"},
    "admin@example.com": {"password": "admin123", "name": "Admin User"},
}

# Load test data from JSON files
def load_test_data(filename):
    """Load test data from data directory."""
    path = DATA_DIR / filename
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {}


def audit_log(action, details, username="anonymous"):
    """Write an audit log entry."""
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "username": username,
        "action": action,
        "details": details,
    }
    log_file = LOGS_DIR / "audit.log"
    with open(log_file, "a") as f:
        f.write(json.dumps(log_entry) + "\n")


def require_login(f):
    """Decorator to require login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


# ============================================================================
# UI Routes
# ============================================================================

@app.route("/")
def index():
    """Home page - redirect to dashboard if logged in, else to login."""
    if "user" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login page and handler."""
    error = None
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        
        if not email or not password:
            error = "Email and password are required"
        elif email not in VALID_USERS:
            error = "Invalid email or password"
            audit_log("login_attempt_failed", {"email": email, "reason": "user_not_found"})
        elif VALID_USERS[email]["password"] != password:
            error = "Invalid email or password"
            audit_log("login_attempt_failed", {"email": email, "reason": "invalid_password"})
        else:
            # Login successful
            session["user"] = email
            session["name"] = VALID_USERS[email]["name"]
            audit_log("login_successful", {"email": email}, username=email)
            return redirect(url_for("dashboard"))
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Login - SaaS App</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 50px; }
            .login-form { max-width: 400px; }
            input { margin: 10px 0; padding: 8px; width: 100%; box-sizing: border-box; }
            button { padding: 10px 20px; background-color: #007bff; color: white; border: none; cursor: pointer; }
            button:hover { background-color: #0056b3; }
            .error { color: red; margin: 10px 0; }
            .success { color: green; margin: 10px 0; }
        </style>
    </head>
    <body>
        <h1>Login</h1>
        """ + (f'<div class="error">{error}</div>' if error else "") + """
        <form method="post" class="login-form">
            <input type="email" name="email" placeholder="Email" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
        <hr>
        <p><strong>Test Credentials:</strong></p>
        <ul>
            <li>testuser@example.com / password123</li>
            <li>admin@example.com / admin123</li>
        </ul>
    </body>
    </html>
    """
    return html


@app.route("/dashboard")
@require_login
def dashboard():
    """Dashboard page."""
    username = session.get("name", "User")
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dashboard - SaaS App</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 50px; }}
            .header {{ display: flex; justify-content: space-between; align-items: center; }}
            .nav {{ margin: 20px 0; }}
            a {{ margin-right: 15px; text-decoration: none; color: #007bff; }}
            a:hover {{ text-decoration: underline; }}
            .success {{ color: green; margin: 10px 0; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Dashboard</h1>
            <span>Welcome, {username}!</span>
        </div>
        <div class="nav">
            <a href="{url_for('submit_form')}">Submit Form</a>
            <a href="{url_for('export_report')}">Export Report</a>
            <a href="{url_for('logout')}">Logout</a>
        </div>
        <p>You are logged in. Use the navigation above.</p>
    </body>
    </html>
    """
    return html


@app.route("/form", methods=["GET", "POST"])
@require_login
def submit_form():
    """Form submission page."""
    success = False
    error = None
    
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()
        
        if not name or not email or not message:
            error = "All fields are required"
        elif len(message) < 10:
            error = "Message must be at least 10 characters"
        else:
            # Save form data
            forms_file = DATA_DIR / "forms.json"
            forms = load_test_data("forms.json")
            if "submissions" not in forms:
                forms["submissions"] = []
            
            forms["submissions"].append({
                "timestamp": datetime.utcnow().isoformat(),
                "name": name,
                "email": email,
                "message": message,
                "submitted_by": session.get("user"),
            })
            
            forms_file.write_text(json.dumps(forms, indent=2))
            audit_log("form_submitted", {"name": name, "email": email}, username=session.get("user"))
            success = True
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Submit Form - SaaS App</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 50px; }}
            .form-container {{ max-width: 500px; }}
            input, textarea {{ margin: 10px 0; padding: 8px; width: 100%; box-sizing: border-box; }}
            button {{ padding: 10px 20px; background-color: #007bff; color: white; border: none; cursor: pointer; }}
            button:hover {{ background-color: #0056b3; }}
            .error {{ color: red; margin: 10px 0; }}
            .success {{ color: green; margin: 10px 0; }}
            a {{ color: #007bff; text-decoration: none; }}
        </style>
    </head>
    <body>
        <h1>Submit Form</h1>
        <a href="{url_for('dashboard')}">← Back to Dashboard</a>
        
        """ + (f'<div class="success">Form submitted successfully!</div>' if success else "") + """
        """ + (f'<div class="error">{error}</div>' if error else "") + """
        
        <form method="post" class="form-container">
            <input type="text" name="name" placeholder="Your Name" required>
            <input type="email" name="email" placeholder="Your Email" required>
            <textarea name="message" placeholder="Your Message (min 10 chars)" required></textarea>
            <button type="submit">Submit</button>
        </form>
    </body>
    </html>
    """
    return html


@app.route("/export")
@require_login
def export_report():
    """Generate and download an export report."""
    import csv
    from io import StringIO
    
    # Create a CSV export
    forms_data = load_test_data("forms.json")
    submissions = forms_data.get("submissions", [])
    
    export_file = REPORTS_DIR / "export.csv"
    with open(export_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "name", "email", "message"])
        writer.writeheader()
        for row in submissions:
            writer.writerow(row)
    
    audit_log("export_generated", {"file": "export.csv", "rows": len(submissions)}, username=session.get("user"))
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Export - SaaS App</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 50px; }}
            .success {{ color: green; }}
        </style>
    </head>
    <body>
        <h1>Export Report</h1>
        <div class="success">✓ Export generated successfully!</div>
        <p>File saved: {export_file.name}</p>
        <p>Total records exported: {len(submissions)}</p>
        <a href="{url_for('dashboard')}">← Back to Dashboard</a>
    </body>
    </html>
    """
    return html


@app.route("/logout")
def logout():
    """Logout."""
    user = session.get("user")
    session.clear()
    audit_log("logout", {}, username=user)
    return redirect(url_for("login"))


# ============================================================================
# API Routes
# ============================================================================

@app.route("/api/auth/login", methods=["POST"])
def api_login():
    """API login endpoint."""
    data = request.get_json()
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()
    
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400
    
    if email not in VALID_USERS:
        audit_log("api_login_failed", {"email": email, "reason": "user_not_found"})
        return jsonify({"error": "Invalid email or password"}), 401
    
    if VALID_USERS[email]["password"] != password:
        audit_log("api_login_failed", {"email": email, "reason": "invalid_password"})
        return jsonify({"error": "Invalid email or password"}), 401
    
    audit_log("api_login_successful", {"email": email}, username=email)
    return jsonify({
        "success": True,
        "user": {
            "email": email,
            "name": VALID_USERS[email]["name"],
        },
        "token": f"token-{email}-{datetime.utcnow().isoformat()}",
    }), 200


@app.route("/api/forms", methods=["POST"])
def api_submit_form():
    """API form submission endpoint."""
    data = request.get_json()
    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    message = data.get("message", "").strip()
    
    errors = {}
    if not name:
        errors["name"] = "Name is required"
    if not email:
        errors["email"] = "Email is required"
    if not message:
        errors["message"] = "Message is required"
    elif len(message) < 10:
        errors["message"] = "Message must be at least 10 characters"
    
    if errors:
        return jsonify({"error": "Validation failed", "details": errors}), 400
    
    forms = load_test_data("forms.json")
    if "submissions" not in forms:
        forms["submissions"] = []
    
    forms["submissions"].append({
        "timestamp": datetime.utcnow().isoformat(),
        "name": name,
        "email": email,
        "message": message,
    })
    
    forms_file = DATA_DIR / "forms.json"
    forms_file.write_text(json.dumps(forms, indent=2))
    audit_log("api_form_submitted", {"name": name}, username="api")
    
    return jsonify({"success": True, "message": "Form submitted"}), 201


@app.route("/api/export", methods=["POST"])
def api_export():
    """API export endpoint."""
    forms_data = load_test_data("forms.json")
    submissions = forms_data.get("submissions", [])
    
    audit_log("api_export_requested", {"rows": len(submissions)}, username="api")
    
    return jsonify({
        "success": True,
        "export_file": "export.csv",
        "total_records": len(submissions),
        "timestamp": datetime.utcnow().isoformat(),
    }), 200


@app.route("/api/users", methods=["GET"])
def api_list_users():
    """API endpoint to list users (for testing)."""
    return jsonify({
        "users": [
            {"email": email, "name": data["name"]}
            for email, data in VALID_USERS.items()
        ]
    }), 200


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
