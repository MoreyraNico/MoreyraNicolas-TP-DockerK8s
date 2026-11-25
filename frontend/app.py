import os
import socket
from flask import Flask, render_template

app = Flask(__name__)

# URL del backend: lee la variable de entorno (para Docker/K8s) o usa localhost por defecto
BACKEND_URL = os.getenv("BACKEND_URL", "/api")

@app.route("/")
def index():
    # Renderiza index.html y le pasa la URL del backend al navegador
    return render_template("index.html", backend_url=BACKEND_URL, replica_id=socket.gethostname())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
