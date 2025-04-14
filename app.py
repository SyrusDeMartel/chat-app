from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit, join_room, leave_room
import os
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')
users = {}  # session_id -> username

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Socket events
@socketio.on('connect')
def handle_connect():
    print(f"[+] A user connected: {request.sid}")

@socketio.on('join')
def handle_join(username):
    users[request.sid] = username
    join_msg = f"👤 {username} has joined the chat"
    broadcast_message(join_msg)

@socketio.on('disconnect')
def handle_disconnect():
    username = users.get(request.sid, "A user")
    leave_msg = f"❌ {username} has left the chat"
    broadcast_message(leave_msg)
    users.pop(request.sid, None)

@socketio.on('message')
def handle_message(msg):
    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
    full_msg = f"[{timestamp}] {msg}"
    print(full_msg)
    append_and_rotate_history(full_msg)
    send(full_msg, broadcast=True)

@socketio.on('typing')
def handle_typing(username):
    emit("show_typing", username, broadcast=True, include_self=False)

def broadcast_message(msg):
    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
    full_msg = f"[{timestamp}] {msg}"
    append_and_rotate_history(full_msg)
    send(full_msg, broadcast=True)

def append_and_rotate_history(new_line):
    history_path = "chat_history.txt"

    if os.path.exists(history_path):
        with open(history_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    else:
        lines = []

    lines.append(new_line + "\n")
    lines = lines[-100:]

    with open(history_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port)
