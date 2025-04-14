from flask import Flask, render_template, request, send_from_directory
from flask_socketio import SocketIO, send, emit, join_room, leave_room
import os
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['UPLOAD_FOLDER'] = 'uploads'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

users = {}
chat_history_file = 'chat_history.txt'

# Ensure upload and screenshots folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('screenshots', exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@socketio.on('connect')
def on_connect():
    print(f"[+] User connected: {request.sid}")

@socketio.on('join')
def on_join(username):
    users[request.sid] = username
    msg = f"👋 {username} joined the chat"
    send(msg, broadcast=True)
    socketio.emit('update_users', list(users.values()))

@socketio.on('disconnect')
def on_disconnect():
    username = users.pop(request.sid, "A user")
    msg = f"❌ {username} left the chat"
    send(msg, broadcast=True)
    socketio.emit('update_users', list(users.values()))

@socketio.on('message')
def on_message(data):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    message = f"[{timestamp}] {data}"
    save_message(message)
    print(message)
    send(message, broadcast=True)

@socketio.on('typing')
def on_typing(username):
    emit("show_typing", username, broadcast=True, include_self=False)

@socketio.on('upload_file')
def handle_file_upload(data):
    filename = data['filename']
    filedata = data['filedata']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    with open(filepath, 'wb') as f:
        f.write(bytes(filedata.encode('latin1')))

    file_msg = f"📎 File shared: {filename} — http://localhost:5000/uploads/{filename}"
    send(file_msg, broadcast=True)

def save_message(msg):
    with open(chat_history_file, 'a', encoding='utf-8') as f:
        f.write(msg + '\n')

if __name__ == '__main__':
    socketio.run(app, debug=True)
