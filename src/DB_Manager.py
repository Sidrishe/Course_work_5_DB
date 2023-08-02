import psycopg2


class DBManager:
    """Класс для работы с БД"""

    def __init__(self, dbname):
        self.host = 'localhost'
        self.dbname = dbname
        self.user = 'postgres'
        self.password = 'Qwerty123'

    def connect(self):
        conn = psycopg2.connect(
            host=self.host,
            dbname=self.dbname,
            user=self.user,
            password=self.password
        )
        return conn
