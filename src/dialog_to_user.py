from src.utils import add_table_data, create_table, csv_writer, clear_table, connection
from src.DB_Manager import DBManager


def user_interaction():
    """Функция для взаимодействия с пользователем"""

    create_db = input('Привет! Введите название вакансии для формирования Базы Данных:  \n')
    csv_writer(create_db)
    create_table()
    clear_table()
    add_table_data()
    connection.close()

    client = DBManager('Vac_DB')

    while True:
        try:
            choice_user = int(input(
                f'''Выберите нужное: 
1 - Чтобы получить список всех компаний и количество вакансий у каждой компании
2 - Получить список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
3 - Получить среднюю зарплату по вакансия
4 - Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям
5 - Получает список всех вакансий, в названии которых содержатся переданные в метод слова,например "python"
0 - Завершить работу программы\n'''))

            if choice_user in [1, 2, 3, 4, 5]:
                if choice_user == 1:
                    get_companies_and_vac = client.get_companies_and_vacancies_count()
                    for v in get_companies_and_vac:
                        print(v)
                elif choice_user == 2:
                    get_all_vac = client.get_all_vacancies()
                    for v in get_all_vac:
                        print(v)
                elif choice_user == 3:
                    get_avg_sal = client.get_avg_salary()
                    print(get_avg_sal)
                elif choice_user == 4:
                    get_vac_with_hig = client.get_vacancies_with_higher_salary()
                    for v in get_vac_with_hig:
                        print(v)
                elif choice_user == 5:
                    user_query = input('Введите ключевое слово для запроса: ')
                    get_vac_with_key = client.get_vacancies_with_keyword(user_query)
                    for v in get_vac_with_key:
                        print(v)
            elif choice_user == 0:
                break
            else:
                raise ValueError
        except ValueError:
            print("\nНекорректный ввод")
