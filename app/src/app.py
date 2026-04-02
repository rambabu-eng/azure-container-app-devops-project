from flask import Flask, render_template, jsonify
from mssql_python import connect
import os

app = Flask(__name__)

def get_sql_connection():
    server = os.getenv("SQL_SERVER")
    database = os.getenv("SQL_DATABASE")
    username = os.getenv("SQL_USER")
    password = os.getenv("SQL_PASSWORD")

    connection_string = (
        f"Server={server},1433;"
        f"Database={database};"
        f"UID={username};"
        f"PWD={password};"
        f"Encrypt=yes;"
        f"TrustServerCertificate=no;"
    )
    return connect(connection_string)

@app.route("/")
def home():
    app_name = os.getenv("APP_NAME", "Secure Containerised Web App")
    environment = os.getenv("ENVIRONMENT", "Development")
    version = os.getenv("APP_VERSION", "v1")
    secret = os.getenv("MY_SECRET", "No Secret Found")

    db_status = "Not tested"
    try:
        conn = get_sql_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM dbo.Visitors")
        row = cursor.fetchone()
        db_status = f"Connected - Visitors count: {row[0]}"
        conn.close()
    except Exception as e:
        db_status = f"DB connection failed: {str(e)}"

    return render_template(
        "index.html",
        app_name=app_name,
        environment=environment,
        version=version,
        secret=secret,
        db_status=db_status
    )

@app.route("/dbhealth")
def dbhealth():
    try:
        conn = get_sql_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT TOP 5 Id, Name, VisitTime FROM dbo.Visitors ORDER BY Id DESC")
        rows = cursor.fetchall()
        conn.close()
        return jsonify({
            "status": "connected",
            "rows": [list(r) for r in rows]
        }), 200
    except Exception as e:
        return jsonify({
            "status": "failed",
            "error": str(e)
        }), 500

@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)