import requests
from bs4 import BeautifulSoup

from enums.course_year import CourseYear

base_url = "https://fmi-plovdiv.org/"

def get_latest_news():
    response = requests.get(f'{base_url}news.jsp?ln=1&id=2')
    soup = BeautifulSoup(response.text, 'html.parser')
    a_tags = soup.find_all('a')
    links = [{'text': tag.get_text(strip=True), 'href': tag.get('href')}
             for tag in a_tags if tag.get('href') and
             tag.get('href').startswith('news.jsp') and 'newsPageNumber' in tag.get('href')]
    return to_html_a_tag(links)


def get_program_url(student_info):

    major_schedule = get_major_schedule()
    major_schedule_href = get_href_from_student_major(student_info.major, major_schedule)

    response = requests.get(base_url + major_schedule_href)
    soup = BeautifulSoup(response.text, 'html.parser')
    page_content = soup.find('table', class_='edu_gratbl')
    table_rows = page_content.find_all('tr')

    for row in table_rows:
        row_cols = row.find_all('td')
        if row_cols:
            first_td = row_cols[0]
            course_label_year = first_td.find_all('p')[0].get_text(strip=True)
            if len(course_label_year) == 0:
                continue
            if student_info.university_year == CourseYear.get_course_year(course_label_year):
                return build_program_url(row_cols, student_info, course_label_year)

    return None

def build_program_url(cols, student_info, course_label_year):
    print(cols[1])
    second_td = cols[1]
    link = second_td.find_all('a')
    url = base_url + link[0].get('href')
    return f'<a href="{url}" target="_blank">{student_info.major} - {course_label_year}</a>'


def get_major_schedule():
    response = requests.get(f'{base_url}index.jsp?ln=1&id=1382')
    soup = BeautifulSoup(response.text, 'html.parser')
    page_content = soup.find('div', class_='pageContent')
    a_tags = page_content.find_all('a')
    links = [{'text': tag.get_text(strip=True), 'href': tag.get('href')}
             for tag in a_tags if tag.get('href') and
             tag.get('href').startswith('index.jsp') and 'ln' in tag.get('href')]
    return links

def get_inspectors():
    response = requests.get(f'{base_url}index.jsp?ln=1&id=2363')
    soup = BeautifulSoup(response.text, 'html.parser')
    page_content = soup.find('div', class_='pageContent')
    tr_tags = page_content.find_all('tr')
    links = [{'text': tag.get_text(strip=True), 'td': tag.get('td')}
             for tag in tr_tags if tag.get('td') and
             tag.get('td').startswith('index.jsp') and 'ln' in tag.get('td')]
    return links

def get_major_schedule_links():
    return to_html_a_tag(get_major_schedule())


def get_href_from_student_major(major, fields_list):
    for field_info in fields_list:
        if field_info['text'] == major:
            return field_info['href']
    return None

def to_html_a_tag(links):
    return [f'<a href="{base_url + link["href"]}">{link["text"]}</a>' for link in links]