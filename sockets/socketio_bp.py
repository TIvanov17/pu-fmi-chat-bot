from flask_socketio import SocketIO, emit
from flask import Blueprint
from service.html_parser_service import get_latest_news

socketio_bp = Blueprint('socketio_bp', __name__)
socketio = SocketIO()

@socketio.on('user_message')
def handle_user_message(message):
    print(f"User: {message}")
    # emit('bot_reply', 'Hello, how can I assist you?')

    if 'новини' in message.lower():
        links = get_latest_news()
        if links:
            response = 'Последните новини\n\n'
            for link in links:
                #response += f'<li><a href="{link["href"]}" target="_blank">{link["text"]}</a></li>'
                response += f'* {link["text"]}\n\n'
        else:
            response = "No links found matching the criteria."

        emit('bot_reply', response)
    else:
        emit('bot_reply', "Send a message containing 'новини' to get news links.")
