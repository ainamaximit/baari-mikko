class Dbq:
    def __init__(self):
        print('lol')
        self.create_connection(
            "test1", "mikko", "baari", "127.0.0.1"
        )
    connection = None

    def create_connection(self, db_name, db_user, db_password, db_host):
        try:
            self.connection = psycopg2.connect(
                database=db_name,
                user=db_user,
                password=db_password,
                host=db_host,
            )
            print("Connection to PostgreSQL DB successful")
        except OperationalError as e:
            print(f"The error '{e}' occurred in db_query.py create_connection()")


    def executemany_insert_query(self, query, vars):
        cursor = self.connection.cursor()
        try:
            cursor.executemany(query, vars)

            self.connection.commit()
            print("Query executed successfully")
            cursor.close()
            self.connection.close()
            return True

        except DatabaseError as e:
            print(f"The error '{e}' occurred in db_query.py executemany_insert_query()")
            return False


    # gets connection, query and vars to plug in
    def execute_insert_query(self, query, vars):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, vars)
            self.connection.commit()
            print("Query executed successfully")
            cursor.close()
            self.connection.close()
            return True

        except DatabaseError as e:
            print(f"The error '{e}' occurred in db_query.py execute_insert_query()")
            return False


    def execute_read_query(self, query, vars):
        cursor = self.connection.cursor()

        try:
            cursor.execute(query, vars)
            result = cursor.fetchall()
            cursor.close()
            self.connection.close()
            return result

        except DatabaseError as e:
            print(f"The error '{e}' occurred in db_query.py execute_read_query()")


    def all_drinks(self):

        vars = (None,)

        result = self.execute_read_query(query, vars)
        return result


    def available_drinks(self):

        vars = (None,)

        result = self.execute_read_query(query, vars)
        return result


    # Gets drink name
    # Rerturn recipe if available else None
    def availble_recipe(self, drink):

        vars = (drink,)

        result = self.execute_read_query(query, vars)
        print(result)
        if len(result) > 0:
            return dict(result)
        else:
            return None


    def recipe(self, drink):

        vars = (drink,)

        result = self.execute_read_query(query, vars)
        if len(result) > 0:
            return list(map(list, result))
        else:
            return None


    def all_recipes(self):

        vars = (None,)

        result = self.execute_read_query(query, vars)

        print(result)
        return result


    def all_ingredients(self):

        vars = (None,)

        result = self.execute_read_query(query, vars)

        print(result)
        return result


    def insert_recipe(self, id, drink_id, ingredient_id, quantity):
        query = """
        INSERT INTO recipes (id, drink_id, ingredient_id, quantity)
        VALUES (%s,%s,%s,%s)
        ON CONFLICT (id)
        DO UPDATE SET drink_id = EXCLUDED.drink_id, ingredient_id = EXCLUDED.ingredient_id, quantity = EXCLUDED.quantity;
        """

        variables = (id, drink_id, ingredient_id, quantity)

        self.executemany_insert_query(query, variables)

        return True


    def create_user(self, name, face_encoding, img_path, admin):


        vars = (name, face_encoding, img_path, admin)

        return self.execute_insert_query(query, vars)


    def users_faces(self):

        vars = (None,)

        result = self.execute_read_query(query, vars)
        return result


    def users_names(self):

        vars = (None,)

        names = self.execute_read_query(query, vars)
        result = [i[0] for i in names]

        print(result)
        return result


    def users(self):

        vars = (None,)

        result = self.execute_read_query(query, vars)

        print(result)
        return result


    def delete_user(self, id):

        vars = (id,)

        result = self.execute_insert_query(query, vars)

        print(result)
        return result


    def all_ingredients(self):

        vars = (None,)

        result = self.execute_read_query(query, vars)

        return result


if __name__ == '__main__':
    print('lol')
