from flask import Flask, jsonify
import os

app = Flask(__name__)

# Get version from environment variable (set by Docker/Jenkins)
VERSION = os.getenv("APP_VERSION", "v1")

@app.route("/")
def home():
    return f"🚀 Flask App is running fine! Version: {VERSION}"

@app.route("/health")
def health():
    return jsonify(status="healthy"), 200

@app.route("/version")
def version():
    return jsonify(version=VERSION)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
