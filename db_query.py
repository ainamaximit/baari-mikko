import psycopg2
import sys

# Using PostgreSQL 13.2 with database test1.pgsql

# Improve: serious duplication must be removed

# Ask recipe for drink if available. Else return 'Drink not available'.
def recipe(drink):
    recipe = None
    con = None

    # If connection works
    try:

        con = psycopg2.connect(host='localhost', database='test1', user='mikko',
            password='baari')

        cur = con.cursor()

        # Join neccesary tables and ask for drink recipe if possible to make
        cur.execute("SELECT quantity, pumps.id FROM drinks JOIN recipes ON drinks.id = recipes.drink_id JOIN ingredients ON recipes.ingredient_id = ingredients.id LEFT JOIN pumps ON pumps.ingredient_id = ingredients.id WHERE drink=%s AND pumps.ingredient_id IS NOT NULL", (drink,))

        # If there is recipe print it
        if cur.rowcount > 0:
            # for record in cur:
            #     print(record)
            recipe = cur.fetchall()
            print(recipe)
        else:
            print('Drink not available.')

    # Else report error and exit
    except psycopg2.DatabaseError as e:

        print(f'Error {e}')
        sys.exit(1)

    # after close connection
    finally:

        if con:
            con.close()
    return recipe

def get_drinks():
    drinks = None
    con = None

    # If connection works
    try:

        con = psycopg2.connect(host='localhost', database='test1', user='mikko',
            password='baari')

        cur = con.cursor()

        # Join neccesary tables and ask for drink recipe if possible to make
        cur.execute("SELECT drink FROM drinks")

        # If there is recipe print it
        if cur.rowcount > 0:
            # for record in cur:
            #     print(record)
            drinks = cur.fetchall()
            print(drinks)
        else:
            print('No drinks')

    # Else report error and exit
    except psycopg2.DatabaseError as e:

        print(f'Error {e}')
        sys.exit(1)

    # after close connection
    finally:

        if con:
            con.close()
    return drinks


if __name__ == '__main__':
    # drink to make
    get_drinks()
    drink = 'Rommicola'
    recipe(drink)
