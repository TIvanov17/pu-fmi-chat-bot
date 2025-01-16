from flask import Blueprint, request, render_template, jsonify
from bs4 import BeautifulSoup
import eventlet
import requests
from service.core_service import find_messages

home = Blueprint('home', __name__)

@home.route('/')
def index():
    return render_template('index.html')

@home.route('/messages')
def get_all_messages():
    return jsonify(find_messages())
