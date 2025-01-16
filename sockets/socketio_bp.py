from flask_socketio import SocketIO, emit
from flask import Blueprint, request
from service.curriculum_service import is_curriculum_topic, handle_curriculum_topic
from service.html_parser_service import get_latest_news, get_major_schedule_links
from database.db import get_last_conversation_message, insert_conversation
from service.core_service import  get_link_of_schedule_by_faculty_number

socketio_bp = Blueprint('socketio_bp', __name__)
socketio = SocketIO()

@socketio.on("connect")
def handle_disconnect():
    user_id = request.sid
    insert_conversation(user_id, "New user connected")
    emit("connected", {"message": "Welcome! You are connected." + user_id})

@socketio.on('user_message')
def handle_user_message(message):
    user_id = request.sid
    insert_conversation(user_id, message)
    # emit("bot_reply", get_link_of_schedule_by_faculty_number(message))

    if 'програма' in message.lower():
        emit("bot_reply", "Въведете факултетен номер:")
        return

    last_message = get_last_conversation_message(user_id)
    response = ''
    if last_message and last_message[0].lower() == "програма":
        if message.isdigit() and len(message) == 10:
            emit("bot_reply", get_link_of_schedule_by_faculty_number(message))
        return
    elif 'новини' in message.lower():
        links = get_latest_news()
        if links:
            response = 'Последните новини\n\n'
            for link in links:
                response += f'* {link}\n\n'
        emit('bot_reply', response)
    elif is_curriculum_topic(message):
        emit('bot_reply', handle_curriculum_topic(message))
    elif 'разписание' in message.lower():
        links = get_major_schedule_links()
        if links:
            response = 'Факултет по математика и информатика - Учебни разписания\n\n'
            for link in links:
                response += f'* {link}\n\n'
        emit('bot_reply', response)
    else:
        emit('bot_reply', "Error")

def get_href_from_dto(student_info_dto, fields_list):
    for field_info in fields_list:
        if field_info['text'] == student_info_dto.field:
            return field_info['href']
    return None