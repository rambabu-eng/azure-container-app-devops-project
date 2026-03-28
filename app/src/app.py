from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route("/")
def home():
    app_name = os.getenv("APP_NAME", "Secure Containerised Web App")
    environment = os.getenv("ENVIRONMENT", "Development")
    version = os.getenv("APP_VERSION", "v1")

    return render_template(
        "index.html",
        app_name=app_name,
        environment=environment,
        version=version
    )

@app.route("/health")
def health():
    return {
        "status": "healthy",
        "app": "containerised-web-app"
    }, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)