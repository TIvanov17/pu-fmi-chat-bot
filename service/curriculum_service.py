import spacy
import requests
from bs4 import BeautifulSoup

# absolute tragic bullchocolate

nlp = spacy.load("mk_core_news_sm")

CURRICULUM_INTENTS = {
    "график": ["учебен график", "дай график"],
    "план": ["график план", "искам план", "дай ми план", "учебни разписания"],
    "сесии": ["график сесии", "сесията", "кога е сесията", "изпитни сесии"],
    "изпити": ["график изпити", "дай изпити", "изпити", "държавни изпити"],
    "календар": ["график календар", "календар", "дай календара", "академичен календар"]
}


def detect_topic(message):
    doc = nlp(message.lower())
    for topic, keywords in CURRICULUM_INTENTS.items():
        if any(keyword in doc.text for keyword in keywords):
            return topic
    return None


def is_curriculum_topic(message):
    if not isinstance(message, str) or not message.strip():
        return False
    return detect_topic(message) is not None


def handle_curriculum_topic(message):
    topic = detect_topic(message)
    if 'график' == topic:
        return get_schedule_content()
    elif 'календар' == topic:
        return get_academic_calendar()
    else:
        return topic


def get_schedule_content():
    content = get_content("https://fmi-plovdiv.org/index.jsp?ln=1&id=52")
    return get_common_links("Моля напишете, кое ви интересува", content.find_all("a"))


def get_academic_calendar():
    base_url = 'https://fmi-plovdiv.org/'
    content = get_content("https://fmi-plovdiv.org/index.jsp?id=65&ln=1")
    links = content.find_all('a')[:2]
    response = 'Академичните календари са:\n\n'
    response += create_link(base_url + links[0]["href"], "За бакалавър")
    response += "\n\n"
    response += create_link(base_url + links[1]["href"], "За магистър")
    return response

# Util methods


def get_common_links(head, links):
    response = head + ': \n\n'
    for link in links:
        response += f'* {link.get_text()}\n\n'
    return response.replace("* ", "")


def is_master(message):
    return any(keyword in message for keyword in ['магистър', 'магистърски', 'магистарска'])


def get_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.find_all('div', class_="pageContent")[0]


def create_link(url, text):
    return f'<a href="{url}" target="_blank">{text}</a>'
