from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import eventlet  # Add this import for Eventlet

eventlet.monkey_patch()

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def home():
    return render_template('index.html')

@socketio.on('user_message')
def handle_user_message(message):
    print(f"User: {message}")
    emit('bot_reply', 'Hello, how can I assist you?')

if __name__ == '__main__':
    socketio.run(app, debug=True)
