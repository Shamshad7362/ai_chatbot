import os
import secrets

import markdown
from ai_service import Chatbot
from config import OPEN_ROUTERAI_API_KEY
from flask import Flask, Response, redirect, render_template, request, session, url_for


app = Flask(
    __name__,
    template_folder="../frontend",
    static_folder="../frontend/assets",
)
# Configure FLASK_SECRET_KEY in .env when deploying the app.
app.secret_key = os.getenv("FLASK_SECRET_KEY") or secrets.token_hex(32)

# Chat histories stay on the server and are separated by the browser's session ID.
chatbots_by_session = {}
MODEL = "apodex/apodex-1.1-mini:free"


def get_chatbot():
    session_id = session.get("chat_id")
    if session_id is None:
        session_id = secrets.token_urlsafe(24)
        session["chat_id"] = session_id

    if session_id not in chatbots_by_session:
        chatbot = Chatbot(api_key=OPEN_ROUTERAI_API_KEY)
        chatbot.model = MODEL
        chatbots_by_session[session_id] = chatbot

    return chatbots_by_session[session_id]


def get_display_history(chatbot):
    history = []
    for message in chatbot.messages:
        role = message.get("role")
        content = message.get("content")
        if role == "user" and content is not None:
            history.append({"role": "user", "content": content})
        elif role == "assistant" and content:
            history.append({
                "role": "assistant",
                "content": markdown.markdown(
                    content,
                    extensions=["tables", "fenced_code", "codehilite"],
                ),
            })
    return history


@app.route("/", methods=["GET"])
def index():
    chatbot = get_chatbot()
    return render_template("index.html", history=get_display_history(chatbot))


@app.route("/ask", methods=["POST"])
def ask():
    user_message = request.form.get("message", "").strip()
    if user_message:
        get_chatbot().ask(user_message)

    # Post/Redirect/Get: browser refresh repeats this GET, not the POST.
    return redirect(url_for("index"))


@app.route("/stream", methods=["POST"])
def stream():
    body = request.get_json(silent=True) or {}
    user_message = body.get("message", "").strip()
    if not user_message:
        return Response("Message is required.", status=400, mimetype="text/plain")

    return Response(
        get_chatbot().ask_stream(user_message),
        mimetype="text/plain",
    )


if __name__ == "__main__":
    app.run(debug=True)
