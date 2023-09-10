from flask import Flask, render_template, request
import csv
from urllib.parse import urlparse, parse_qs
import re 

app = Flask(__name__)

# Загрузка данных из CSV файла
data = []
with open('combined_divs3.csv', 'r', newline='', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        data.append(row)

# Основная страница
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_query = request.form['search_query']
        results = search_in_csv(search_query)
        return render_template('index.html', results=results, search_query=search_query)
    return render_template('index.html', results=None, search_query=None)

import re
import html2text

def clean_paragraph(paragraph_html):
    # Инициализируем конвертер
    converter = html2text.HTML2Text()
    # Устанавливаем параметры конвертации
    converter.ignore_links = True  # Игнорировать гиперссылки
    converter.ignore_images = True  # Игнорировать изображения
    converter.ignore_emphasis = True  # Игнорировать выделение (например, курсив)

    # Преобразуем HTML в текст с использованием конвертера
    cleaned_text = converter.handle(paragraph_html)

    # Удаляем символы перевода строки (\n) с использованием регулярного выражения
    cleaned_text = re.sub(r'\\n', '', cleaned_text).strip()

    # Удаляем одинарные кавычки в начале и в конце строки
    cleaned_text = cleaned_text.strip("'")

    return cleaned_text


def search_in_csv(query):
    results = {'молитвы': [], 'мифы': [], 'ритуалы': []}
    seen = set()
    for row in data:
        paragraph, paragraph_html = row
        url = paragraph.strip("[]")
        url = paragraph.strip("'")

        # Разделяем строку на элементы, если они разделены, например, запятой
        paragraph_html_list = paragraph_html.split(',')

        for element in paragraph_html_list:
            if query in element:
                cleaned_paragraph_html = clean_paragraph(element)
                cleaned_paragraph_html = f'<strong>{cleaned_paragraph_html}</strong>'
                result_tuple = (url, cleaned_paragraph_html)
                if result_tuple not in seen:
                    seen.add(result_tuple)
                    # Проверяем, содержит ли URL одно из ключевых слов
                    if 'gebet' in url:
                        category = 'молитвы'
                    elif 'myth' in url:
                        category = 'мифы'
                    elif 'besrit' in url:
                        category = 'ритуалы'
                    else:
                        category = 'другое'  # Вы можете добавить другую категорию по умолчанию, если нужно
                    # Извлекаем значения xst и prgr из URL
                    parsed_url = urlparse(url)
                    xst = parse_qs(parsed_url.query).get('xst', [''])[0]
                    prgr = parse_qs(parsed_url.query).get('prgr', [''])[0]
                    # Формируем текст для ссылки с использованием HTML-сущностей
                    link_text = f"{xst}. &sect;{prgr}"
                    # Сохраняем только элементы div с очищенным текстом
                    results[category].append({'url': url, 'paragraph_html': cleaned_paragraph_html, 'link_text': link_text})
    return results


# Отключите авто-экранирование URL в шаблоне
app.jinja_env.autoescape = False

if __name__ == '__main__':
    app.run(debug=True)
