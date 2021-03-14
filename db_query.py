import psycopg2
from psycopg2 import OperationalError, DatabaseError


def create_connection(db_name, db_user, db_password, db_host):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred in db_query.py create_connection()")
    return connection


def executemany_insert_query(connection, query, vars):
    cursor = connection.cursor()
    try:
        cursor.executemany(query, vars)

        connection.commit()
        print("Query executed successfully")
        cursor.close()
        connection.close()
        return True

    except DatabaseError as e:
        print(f"The error '{e}' occurred in db_query.py executemany_insert_query()")
        return False


# gets connection, query and vars to plug in
def execute_insert_query(connection, query, vars):
    cursor = connection.cursor()
    try:
        cursor.execute(query, vars)
        connection.commit()
        print("Query executed successfully")
        cursor.close()
        connection.close()
        return True

    except DatabaseError as e:
        print(f"The error '{e}' occurred in db_query.py execute_insert_query()")
        return False


def execute_read_query(connection, query, vars):
    cursor = connection.cursor()

    try:
        cursor.execute(query, vars)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result

    except DatabaseError as e:
        print(f"The error '{e}' occurred in db_query.py execute_read_query()")


def get_all_drinks():
    # Connect
    connection = create_connection(
        "test1", "mikko", "baari", "127.0.0.1"
    )

    query = """
    SELECT id, drink FROM drinks
    """
    vars = (None,)

    result = execute_read_query(connection, query, vars)
    return result


def get_available_drinks():
    # Connect
    connection = create_connection(
        "test1", "mikko", "baari", "127.0.0.1"
    )

    query = """
    SELECT DISTINCT drink FROM drinks
    JOIN recipes ON drinks.id = recipes.drink_id
    JOIN ingredients ON recipes.ingredient_id = ingredients.id
    JOIN pumps ON ingredients.id = pumps.ingredient_id
    WHERE pumps.ingredient_id IS NOT NULL
    """
    vars = (None,)

    result = execute_read_query(connection, query, vars)
    return result


# Gets drink name
# Rerturn recipe if available else None
def get_availble_recipe(drink):
    # Connect
    print(drink)
    connection = create_connection(
        "test1", "mikko", "baari", "127.0.0.1"
    )

    query = """
    SELECT pumps.id, quantity FROM drinks
    JOIN recipes ON drinks.id = recipes.drink_id
    JOIN ingredients ON recipes.ingredient_id = ingredients.id
    LEFT JOIN pumps ON pumps.ingredient_id = ingredients.id
    WHERE drink=%s AND pumps.ingredient_id IS NOT NULL
    """
    vars = (drink,)

    result = execute_read_query(connection, query, vars)
    print(result)
    if len(result) > 0:
        return dict(result)
    else:
        return None


def get_recipe(drink):
    # Connect
    connection = create_connection(
        "test1", "mikko", "baari", "127.0.0.1"
    )

    query = """
    SELECT recipes.id, drinks.id, ingredients.id, quantity, drinks.drink, ingredients.ingredient FROM drinks
    JOIN recipes ON drinks.id = recipes.drink_id
    JOIN ingredients ON recipes.ingredient_id = ingredients.id
    WHERE drink=%s
    """
    vars = (drink,)

    result = execute_read_query(connection, query, vars)
    if len(result) > 0:
        return list(map(list, result))
    else:
        return None


def get_recipes():
    # Connect
    connection = create_connection(
        "test1", "mikko", "baari", "127.0.0.1"
    )

    query = """
    SELECT drinks.id, drinks.drink, ingredients.id, ingredients.ingredient, quantity FROM drinks
    JOIN recipes ON drinks.id = recipes.drink_id
    JOIN ingredients ON recipes.ingredient_id = ingredients.id
    """
    vars = (None,)

    result = execute_read_query(connection, query, vars)

    print(result)
    return result


def get_ingredients():
    # Connect
    connection = create_connection(
        "test1", "mikko", "baari", "127.0.0.1"
    )

    query = """
    SELECT * FROM ingredients
    """
    vars = (None,)

    result = execute_read_query(connection, query, vars)

    print(result)
    return result


def insert_recipe(id, drink_id, ingredient_id, quantity):
    connection = create_connection(
        "test1", "mikko", "baari", "127.0.0.1"
    )

    query = """
    INSERT INTO recipes (id, drink_id, ingredient_id, quantity)
    VALUES (%s,%s,%s,%s)
    ON CONFLICT (id)
    DO UPDATE SET drink_id = EXCLUDED.drink_id, ingredient_id = EXCLUDED.ingredient_id, quantity = EXCLUDED.quantity;
    """

    variables = (id, drink_id, ingredient_id, quantity)

    executemany_insert_query(connection, query, variables)

    return True


def create_user(name, face_encoding, img_path, admin):
    connection = create_connection(
        "test1", "mikko", "baari", "127.0.0.1"
    )

    query = """
    INSERT INTO users (name, face, img, admin)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (id)
    DO UPDATE SET name=EXCLUDED.name, face=EXCLUDED.face, img=EXCLUDED.img
    """

    vars = (name, face_encoding, img_path, admin)

    return execute_insert_query(connection, query, vars)


def get_users_faces():
    # Connect
    connection = create_connection(
        "test1", "mikko", "baari", "127.0.0.1"
    )

    query = """
    SELECT * FROM users
    """
    vars = (None,)

    result = execute_read_query(connection, query, vars)
    return result


def get_users_names():
    # Connect
    connection = create_connection(
        "test1", "mikko", "baari", "127.0.0.1"
    )

    query = """
    SELECT name FROM users
    """
    vars = (None,)

    names = execute_read_query(connection, query, vars)
    result = [i[0] for i in names]

    print(result)
    return result


def get_users():
    # Connect
    connection = create_connection(
        "test1", "mikko", "baari", "127.0.0.1"
    )

    query = """
    SELECT id, name, img FROM users
    """
    vars = (None,)

    result = execute_read_query(connection, query, vars)

    print(result)
    return result


def delete_user(id):
    # Connect
    connection = create_connection(
        "test1", "mikko", "baari", "127.0.0.1"
    )

    query = """
    DELETE FROM users
    WHERE id=%s
    """
    vars = (id,)

    result = execute_insert_query(connection, query, vars)

    print(result)
    return result


def get_ingredients():
    # Connect
    connection = create_connection(
        "test1", "mikko", "baari", "127.0.0.1"
    )

    query = """
    SELECT * FROM ingredients
    """
    vars = (None,)

    result = execute_read_query(connection, query, vars)

    return result


if __name__ == '__main__':
    print(get_recipe("Gin Tonic"))
