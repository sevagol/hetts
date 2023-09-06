from flask import Flask, render_template, request
import csv

app = Flask(__name__)

# Загрузка данных из CSV файла
data = []
with open('paragrphs1.csv', 'r', newline='', encoding='utf-8') as csv_file:
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

# Функция для поиска по CSV
# Функция для поиска по CSV и удаления дубликатов
def search_in_csv(query):
    results = []
    seen = set()  # Множество для отслеживания уникальных результатов
    for row in data:
        url, paragraph, paragraph_text = row
        url = url.strip("[]")
        url = url.strip("'")
        paragraph = paragraph.strip("[]")
        paragraph = paragraph.strip("'")
        if query in paragraph_text:
            result_tuple = (url, paragraph)  # Создаем кортеж (URL, параграф)
            if result_tuple not in seen:  # Проверяем, не является ли кортеж дубликатом
                seen.add(result_tuple)
                results.append({'url': url, 'paragraph': paragraph})
    return results


# Отключите авто-экранирование URL в шаблоне
app.jinja_env.autoescape = False


if __name__ == '__main__':
    app.run(debug=True)
