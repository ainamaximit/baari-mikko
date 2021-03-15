import psycopg2
from psycopg2 import OperationalError, DatabaseError


class DatabaseInterface:
    """
    Database interface for PostgreSQL
    TODO
    """
    def __init__(self, db_name, db_user, db_password, db_host):
        self.__db_name = db_name
        self.__db_user = db_user
        self.__db_password = db_password
        self.__db_host = db_host
        self.__connection = None
        self.__create_connection()

    def __create_connection(self):
        """
        Creates connection to database
        :return: None
        """
        try:
            self.__connection = psycopg2.connect(
                database=self.__db_name,
                user=self.__db_user,
                password=self.__db_password,
                host=self.__db_host,
            )
            print("Connection to PostgreSQL DB successful")
        except OperationalError as e:
            print(f"The error '{e}' occurred in db_query.py create_connection()")

    def executemany_query(self, query, *args):
        """
        gets connection, query and vars to plug in
        :param query: sql query to execute
        :param args: list of query %s values
        :return: True if successful
        """
        cursor = self.__connection.cursor()
        try:
            cursor.executemany(query, args)

            self.__connection.commit()
            print("Query executed successfully")
            cursor.close()
            return True

        except DatabaseError as e:
            print(f"The error '{e}' occurred in db_query.py executemany_insert_query()")
            return False

    def execute_query(self, query, args):
        """
        gets connection, query and vars to plug in
        :param query: PostgreSQL query to execute
        :param args: query %s values
        :return: True if successful
        """
        cursor = self.__connection.cursor()
        try:
            cursor.execute(query, args)
            self.__connection.commit()
            print("Query executed successfully")
            cursor.close()
            return True

        except DatabaseError as e:
            print(f"The error '{e}' occurred in DatabaseInterface")
            return False

    def read_query(self, query, *args):
        """
        Reads database tables
        :param query: PostgreSQL query to execute
        :param args: query %s values
        :return: query result
        """
        cursor = self.__connection.cursor()

        try:
            cursor.execute(query, args)
            result = cursor.fetchall()
            cursor.close()
            return result

        except DatabaseError as e:
            print(f"The error '{e}' occurred in db_query.py execute_read_query()")
