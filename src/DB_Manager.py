import psycopg2


class DBManager:
    """Класс для работы с БД"""

    def __init__(self, dbname):
        self.dbname = dbname
        self.user = 'postgres'
        self.password = '{j[kjvf228'
        self.host = 'localhost'

    def connect(self):
        conn = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host
        )
        return conn

    def get_companies_and_vacancies_count(self):
        """Получение названия компании и количество открытых вакансий"""

        conn = self.connect()
        cur = conn.cursor()
        cur.execute("""
            SELECT company_name, COUNT(*) as vacancies_count
            FROM vacancies
            GROUP BY company_name
            ORDER BY vacancies_count DESC
        """)
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result

    def get_all_vacancies(self):
        """Получение всех вакансий"""

        conn = self.connect()
        cur = conn.cursor()
        cur.execute("""
            SELECT company_name, vacancy_name, salary_from, url
            FROM vacancies
            ORDER BY salary_from DESC
        """)
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result

    def get_avg_salary(self):
        """Получение средней з/п"""

        conn = self.connect()
        cur = conn.cursor()
        cur.execute("""
            SELECT AVG(salary_from)
            FROM vacancies
        """)
        result = cur.fetchone()[0]
        cur.close()
        conn.close()
        return result

    def get_vacancies_with_higher_salary(self):
        """Получение информации о вакансии с з/п выше средней по всем вакансиям"""

        avg_salary = self.get_avg_salary()
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(f"""
            SELECT company_name, vacancy_name, salary_from, url
            FROM vacancies
            WHERE salary_from > {avg_salary}
            ORDER BY salary_from DESC
        """)
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result

    def get_vacancies_with_keyword(self, keyword):
        """Получение вакансии по ключевому слову"""

        conn = self.connect()
        cur = conn.cursor()
        cur.execute(f"""
            SELECT company_name, vacancy_name, salary_from, url
            FROM vacancies
            WHERE vacancy_name LIKE '%{keyword}%'
            ORDER BY salary_from DESC
        """)
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result
