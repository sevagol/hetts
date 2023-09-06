from flask import Flask, render_template, request
import csv
from urllib.parse import urlparse, parse_qs

app = Flask(__name__)

# Загрузка данных из CSV файла
data = []
with open('paragrphs2.csv', 'r', newline='', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)
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

# Функция для поиска по CSV и формирования текста для ссылок
# Функция для поиска по CSV и формирования текста для ссылок
def search_in_csv(query):
    results = []
    seen = set()
    for row in data:
        url, paragraph, paragraph_text = row
        url = paragraph.strip("[]")
        url = paragraph.strip("'")
        if query in paragraph_text:
            result_tuple = (url, paragraph)
            if result_tuple not in seen:
                seen.add(result_tuple)
                # Извлекаем значения xst и prgr из URL
                parsed_url = urlparse(url)
                xst = parse_qs(parsed_url.query).get('xst', [''])[0]
                prgr = parse_qs(parsed_url.query).get('prgr', [''])[0]
                # Формируем текст для ссылки с использованием HTML-сущностей
                link_text = f"{xst}. &sect;{prgr}"
                # Сохраняем URL без изменений
                results.append({'url': url, 'paragraph': link_text})
    return results





# Отключите авто-экранирование URL в шаблоне
app.jinja_env.autoescape = False


if __name__ == '__main__':
    app.run(debug=True)
