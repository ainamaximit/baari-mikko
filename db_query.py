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
        print(f"The error '{e}' occurred")
    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

def execute_read_query(connection, query, vars):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query, (vars,))
        result = cursor.fetchall()
        return result
    except DatabaseError as e:
        print(f"The error '{e}' occurred")

def get_all_drinks():
    # Connect
    connection = create_connection(
        "test1", "mikko", "baari", "127.0.0.1"
    )

    query = """
    SELECT drink FROM drinks
    """
    vars = None

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
    vars = None

    result = execute_read_query(connection, query, vars)
    return result

# Gets drink name
# Rerturn recipe if available else None
def get_availble_recipe(drink):
    # Connect
    connection = create_connection(
        "test1", "mikko", "baari", "127.0.0.1"
    )

    query = """
    SELECT quantity, pumps.id FROM drinks
    JOIN recipes ON drinks.id = recipes.drink_id
    JOIN ingredients ON recipes.ingredient_id = ingredients.id
    LEFT JOIN pumps ON pumps.ingredient_id = ingredients.id
    WHERE drink=%s AND pumps.ingredient_id IS NOT NULL
    """
    vars = drink

    result = execute_read_query(connection, query, vars)
    if len(result) > 0:
        return result
    else:
        return None

def Main():
    print(get_all_drinks())
    print(get_available_drinks())
    print(get_availble_recipe('Kelkka'))

if __name__ == '__main__':
    Main()
