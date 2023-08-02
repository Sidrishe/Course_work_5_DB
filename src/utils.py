import csv
import json
import requests
import psycopg2


connection = psycopg2.connect(host='localhost', database="Vac_DB", user='postgres', password='Qwerty123')


def get_vacancies(job_title):
    """Запрос к API HH"""

    params = {
        'text': job_title,
        'per_page': 50
    }

    req = requests.get('https://api.hh.ru/vacancies', params)
    data = req.content.decode()
    req.close()
    js_obj = json.loads(data)
    vac_data = vacancies_pars(js_obj)
    return vac_data


def vacancies_pars(js_obj):
    """Парсинг полученных вакансий"""

    all_vacancy = []
    for obj in js_obj['items']:
        salary = obj.get('salary') or {}
        salary_from = salary.get('from')
        salary_to = salary.get('to')
        if salary_from is not None:
            salary_from = int(salary_from)
        if salary_to is not None:
            salary_to = int(salary_to)

        all_vacancy.append({
            'id': obj['id'],
            'title': obj['name'],
            'salary_from': salary_from or 0,
            'salary_to': salary_to or 0,
            'employer': obj['employer']['name'],
            'url': obj['url'],
            'requirements': obj['snippet']['requirement']
        })

    return all_vacancy


def save_csv(user_input):
    """Сохранение результата запроса в csv файле"""

    cols = ['id', 'title', 'salary_from', 'salary_to', 'employer', 'url', 'requirements']

    with open('vacancies.csv', 'w', newline='', encoding='utf-8') as file:
        wr = csv.DictWriter(file, fieldnames=cols)
        wr.writeheader()
        wr.writerow(get_vacancies(user_input))


def create_table():
    """Создание таблицы в БД"""

    with connection as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                    CREATE TABLE IF NOT EXISTS vacancies(
                        id INT PRIMARY KEY,
                        vacancy_name TEXT,
                        salary_from INT,
                        salary_to INT,
                        company_name TEXT,
                        url TEXT,
                        requirements TEXT
                    );
                """)


def add_table_data():
    """Добавление данных в БД"""

    with connection as conn:
        with conn.cursor() as cursor:
            with open('vacancies.csv', 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    cursor.execute(
                        'INSERT INTO vacancies (id, vacancy_name, salary_from, salary_to, company_name, url, '
                        'requirements) VALUES (%s, %s, %s, %s, %s, %s, %s)', row
                    )


def clear_table():
    """Очистка таблицы в БД"""

    with connection as conn:
        with conn.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE vacancies')


if __name__ == '__main__':
    user_input = input('Введите название вакансии: \n')
    save_csv(user_input)
    create_table()
    clear_table()
    add_table_data()
    connection.close()
    # pass
