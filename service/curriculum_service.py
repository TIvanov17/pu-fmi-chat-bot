import spacy
import requests
from bs4 import BeautifulSoup

# absolute tragic bullchocolate

nlp = spacy.load("mk_core_news_sm")

CURRICULUM_INTENTS = {
    "график": ["учебен график", "дай график"],
    "план": ["график план", "искам план", "дай ми план", "учебни разписания", "план"],
    "сесии": ["график сесии", "сесията", "кога е сесията", "изпитни сесии", 'сесии'],
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
    elif 'план' == topic:
        return get_plans(message)
    elif 'сесии' == topic:
        return get_sessions()
    elif 'изпити' == topic:
        return get_exams()
    elif 'календар' == topic:
        return get_academic_calendar()
    else:
        return topic


def get_sessions():
    return create_link('https://fmi-plovdiv.org/index.jsp?id=70&ln=1', 'More info here')


def get_exams():
    content = get_content('https://fmi-plovdiv.org/index.jsp?id=71&ln=1')
    response = '\n'

    for link in content.find_all('a'):
        response += create_link('https://fmi-plovdiv.org/' + link['href'], link.get_text()) + '\n'
    return response


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


def get_plans(message):
    if is_master(message): return 'Няма пък'

    base_url = 'https://fmi-plovdiv.org/'
    content_url = 'https://fmi-plovdiv.org/index.jsp?id=1382&ln=1'
    content = get_content(content_url)

    response = 'Последните учебните планове са:\n'

    for link in content.find_all('a'):
        response += '\n' + link.get_text() + ':\n'

        link_content = get_content(base_url + link['href'])
        tables = link_content.find_all('table', class_='edu_gratbl')

        for index, table in enumerate(tables):
            # skip the first tr since it is header
            table_trs = table.find_all('tr')[1:]
            response += '    Редовно\n' if index == 0 else 'Задочно\n'

            for row in table_trs:
                col = row.find_all('td')
                response += col[0].find_all('p')[0].get_text()
                response += ' - '
                # get latest td with link (зимен or летен)
                latest_td = col[1] if not col[2].find_all('a') else col[2]

                links_to_attach = []
                for a in latest_td.find_all('a'):
                    links_to_attach.append(create_link(base_url + a['href'], a.get_text()))

                response += ', '.join(links_to_attach)
                response += '\n'
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
