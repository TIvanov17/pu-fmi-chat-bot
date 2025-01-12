from flask import Blueprint, request, render_template, jsonify
from bs4 import BeautifulSoup
import eventlet
import requests
from service.employee_service import find_employees

home = Blueprint('home', __name__)

@home.route('/')
def index():
    return render_template('index.html')

@home.route('/news')
def news():
    pool = eventlet.GreenPool()
    response = requests.get("https://fmi-plovdiv.org/news.jsp?ln=1&id=2")
    soup = BeautifulSoup(response.text, 'html.parser')
    a_tags = soup.find_all('a')
    links = [{'text': tag.get_text(strip=True), 'href': tag.get('href')}
             for tag in a_tags if tag.get('href') and
             tag.get('href').startswith('news.jsp') and 'newsPageNumber' in tag.get('href')]
    print("Status Code:", response.status_code)
    print("Response JSON:", links)
    return jsonify(links)

@home.route('/users')
def get_all_employees():
    return jsonify(find_employees())
