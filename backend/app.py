from markupsafe import escape
from ai_service import Chatbot
from config import OPEN_ROUTERAI_API_KEY
from flask import Flask, render_template, request, jsonify
import markdown
from flask import Response

chatbot = Chatbot(api_key=OPEN_ROUTERAI_API_KEY)
chatbot.model = 'apodex/apodex-1.1-mini:free'



app = Flask(__name__,
            template_folder='../frontend',
            static_folder='../frontend/assets')


@app.route("/",methods=['GET','POST'])
def index():
    return render_template("index.html")

@app.route("/ask",methods=['POST','GET'])
def ask():
    if request.method == 'POST':
        user_msg=request.form.get("message")
        reply_md=chatbot.ask(user_msg)
        # print(reply_md.response.text)
        clean_history=[]
        for m in chatbot.messages:
            if isinstance(m,dict) and "role" in m and "content" in m:
                if m["role"]=="user":
                    clean_history.append({
                        "role": "user",
                        "content": m["content"]
                    })
                if m["role"]=="assistant":
                    clean_history.append({
                        "role": "assistant",
                        "content": markdown.markdown(m["content"],extensions=["tables","fenced_code","codehilite"])
                    })
        return render_template("index.html",history=clean_history)
    else:
        return render_template("index.html")

@app.route("/stream", methods=["POST"])
def stream():
    user_message = request.json.get("message", "")
    return Response(chatbot.ask_stream(user_message), mimetype="text/plain")


if __name__ == "__main__":
    app.run(debug=True)

    