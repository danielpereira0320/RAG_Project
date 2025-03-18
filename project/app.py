from flask import Flask, request, jsonify
from rag_server import ask_question
from update_db import update_collection, clear_entire_history, clear_user_history
from waitress import serve
from chat_history import get_entire_chat

app = Flask(__name__)

@app.route('/chat', methods = ["POST"])
def rag_chat():
    
    data = request.get_json()

    ### takes message - str
    query = data["query"]
    uid = data["uid"]
    
    ### process message
    result = ask_question(query=query, user_id=uid)
    return result

@app.route('/getchatall', methods = ["POST"])
def get_chat_all():
    chat = get_entire_chat()
    return chat

@app.route('/update', methods = ["POST"])
def update_kb():
    doc_count = update_collection()
    return f"{doc_count} documents inserted!"

@app.route('/clearall', methods = ["POST"])
def clear_entire_chat_history():
    clear_entire_history()
    return "Entire chat history reset!"

@app.route('/clearuser', methods = ["POST"])
def clear_user_chat_history():
    data = request.get_json()
    uid = data["uid"]
    clear_user_history(uid)
    return "User chat history reset!"


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000, threads=8)
