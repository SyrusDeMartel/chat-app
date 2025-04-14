from flask import Flask, render_template, request, send_from_directory
from flask_socketio import SocketIO, send, emit, join_room, leave_room

from flask import send_from_directory
from werkzeug.utils import secure_filename

import os
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['UPLOAD_FOLDER'] = 'uploads'

socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

users = {}  # session_id -> username

# Ensure uploads folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# File upload route
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file", 400
    file = request.files['file']
    if file.filename == '':
        return "No filename", 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    return request.host_url + 'uploads/' + filename

# Serve uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


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
    with open("chat_history.txt", "a", encoding="utf-8") as f:
        f.write(full_msg + "\n")
    send(full_msg, broadcast=True)

@socketio.on('typing')
def handle_typing(username):
    emit("show_typing", username, broadcast=True, include_self=False)

def broadcast_message(msg):
    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
    full_msg = f"[{timestamp}] {msg}"
    with open("chat_history.txt", "a", encoding="utf-8") as f:
        f.write(full_msg + "\n")
    send(full_msg, broadcast=True)



if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))  # Use Render-provided PORT
    socketio.run(app, host='0.0.0.0', port=port)
