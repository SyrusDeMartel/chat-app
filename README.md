🔥 Real-Time Chat App

A modern real-time chat application built with **Flask** and **Socket.IO**, featuring:
- 🔒 Admin mode with user-kicking capability
- 🌙 Dark mode toggle
- 💬 Typing indicator
- 📜 Message history (latest 100 messages)
- 📡 Active users list with kick buttons (admin-only)
- ⚡ Fully responsive UI

🚀 Live Demo
👉 https://chat-app-k55e.onrender.com

🧑‍💻 How to Use

1. Choose Role on Entry
- User/Guest: Just enter your name and join the chat.
- Admin: Select "admin" and enter the password (ask the developer if you don’t have it).  
  Admin usernames appear as:
  username (admin)

2. Admin Powers
- Admins can kick any user from the chat.
- A "Kick" button appears next to each username (visible only to admins).

🛠️ Setup Locally

1. Clone the Repo

   git clone https://github.com/your-username/chat-app.git
   cd chat-app

2. Create a Virtual Environment (Optional)

   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate

3. Install Dependencies

   pip install -r requirements.txt

4. Run the App

   python app.py

   Visit http://localhost:5000 in your browser.

📁 Project Structure

chat-app/
│
├── app.py                  # Main Flask server
├── requirements.txt        # Dependencies
├── chat_history.txt        # Stores last 100 messages
├── README.md               # This file
│
├── static/
│   ├── style.css           # Modern responsive styles
│   └── pop.wav             # Notification sound
│
├── templates/
│   └── index.html          # Chat UI
│
├── uploads/                # (Not used currently)
├── screenshots/            # UI previews

💡 Features

- Real-time chat with WebSocket (Socket.IO)
- Admin login with authentication
- Active users with kick control
- Clean UI with dark/light themes
- Message history saved in chat_history.txt
- Scroll to latest messages with notification sound

⚠️ Notes

- Only the latest 100 messages are stored and rotated in chat_history.txt.
- File upload feature has been disabled in this version.
- Admin credentials are not public – contact the developer to gain admin access.

📸 Screenshots

> Add UI previews inside the screenshots/ folder.

📃 License

MIT License – feel free to use and modify!