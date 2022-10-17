import pymysql


class MySql:
    def __init__(self):
        self._connection = None

    def set_connect(self, host, user, password, database):
        self._connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
        )

    def fetch_all(self, query):
        with self._connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        return list(result)


seven_eleven_database = MySql()
seven_eleven_database.set_connect(
    host="test.db",
    user="test",
    password="test",
    database="test",
)
