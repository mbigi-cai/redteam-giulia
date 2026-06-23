"""
Mini web server con HTTP Basic Auth per pubblicare il sito red-team su Render.
Protegge TUTTO (index.html + audio) dietro utente/password.

Le credenziali si leggono dalle variabili d'ambiente:
    BASIC_AUTH_USER       (default: "insiel")
    BASIC_AUTH_PASSWORD   (obbligatoria — impostala su Render, NON nel codice)

Locale:   BASIC_AUTH_USER=insiel BASIC_AUTH_PASSWORD=segreta python3 app.py
Render:   start command  ->  gunicorn app:app --bind 0.0.0.0:$PORT
"""
import os
from flask import Flask, request, Response, send_from_directory

app = Flask(__name__, static_folder=None)
SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")
USER = os.environ.get("BASIC_AUTH_USER", "insiel")
PWD = os.environ.get("BASIC_AUTH_PASSWORD")
REALM = 'Basic realm="Red-Team GiulIA - area riservata"'


def _authorized(auth) -> bool:
    return bool(auth and PWD and auth.username == USER and auth.password == PWD)


@app.before_request
def _guard():
    if not PWD:
        return Response("Configurazione incompleta: manca BASIC_AUTH_PASSWORD.", 500)
    if not _authorized(request.authorization):
        return Response("Accesso riservato.", 401, {"WWW-Authenticate": REALM})
    return None


@app.route("/")
def index():
    return send_from_directory(SITE, "index.html")


@app.route("/<path:path>")
def assets(path):
    return send_from_directory(SITE, path)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    app.run(host="0.0.0.0", port=port)
