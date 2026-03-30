from flask import Flask, render_template, jsonify
import os
import pymssql

app = Flask(__name__)

def get_db_connection():
    server = os.getenv("SQL_SERVER")
    database = os.getenv("SQL_DATABASE")
    username = os.getenv("SQL_USER")
    password = os.getenv("SQL_PASSWORD")

    return pymssql.connect(
        server=server,
        user=username,
        password=password,
        database=database,
        port=1433,
        timeout=10
    )

@app.route("/")
def home():
    app_name = os.getenv("APP_NAME", "Secure Containerised Web App")
    environment = os.getenv("ENVIRONMENT", "Development")
    version = os.getenv("APP_VERSION", "v1")
    secret = os.getenv("MY_SECRET", "No Secret Found")

    db_status = "Not tested"

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT GETDATE()")
        row = cursor.fetchone()
        db_status = f"Connected successfully. SQL time: {row[0]}"
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

@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200

@app.route("/dbhealth")
def dbhealth():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT GETDATE()")
        row = cursor.fetchone()
        conn.close()
        return jsonify({
            "status": "connected",
            "sql_time": str(row[0])
        }), 200
    except Exception as e:
        return jsonify({
            "status": "failed",
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)