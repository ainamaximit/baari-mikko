from databaseinterface import DatabaseInterface
from databasequeries import DatabaseQueries as Dbq
import configparser
import json

config = configparser.ConfigParser()
config.read('config.ini')

dbi = DatabaseInterface(config.get('DATABASE', 'database'),
                        config.get('DATABASE', 'username'),
                        config.get('DATABASE', 'password'),
                        config.get('DATABASE', 'ip_address'))


# impostor
data = {
    "name": "KILLSHOT",
    "ingredients": {
        "Vodka": 50,
        "Rommi": 150
    }
}


# actual functionality to transplant to app.py function

# check drink names and look for match
drink = data["name"]
drinks = dict(dbi.read_query(Dbq.ALL_DRINKS))
print(drinks)
# select right method
# TODO: remove duplicate lines
if drink in drinks.values():
    print('Update Recipe')
    # nuke old recipe
    update_id = dbi.read_query(Dbq.GET_DRINK_ID, (data["name"],))[0][0]
    dbi.execute_query(Dbq.DELETE_RECIPE, (update_id,))

    # iterate over recipe and store to database
    for ingredient, quantity in data["ingredients"].items():
        ingredient_id = dbi.read_query(Dbq.GET_INGREDIENT_ID, (ingredient,))[0][0]
        dbi.execute_query(Dbq.INSERT_RECIPE, (update_id, ingredient_id, quantity))
        print(f"{update_id}, {ingredient_id}, {quantity}")
    print(f"Drink recipe {drink} updated successfully.")

else:
    print('New Recipe')
    try:
        # insert drink name to drinks
        dbi.execute_query(Dbq.INSERT_DRINK, (data["name"],))

        # get drink id
        new_id = dbi.read_query(Dbq.GET_DRINK_ID, (data["name"],))[0][0]
        print(new_id)

        # iterate over recipe and store to database
        for ingredient, quantity in data["ingredients"].items():
            ingredient_id = dbi.read_query(Dbq.GET_INGREDIENT_ID, (ingredient, ))[0][0]
            dbi.execute_query(Dbq.INSERT_RECIPE, (new_id, ingredient_id, quantity))
            print(f"{new_id}, {ingredient_id}, {quantity}")
        print(f"Drink {drink} stored to database successfully.")

    except Exception as e:
        print(f"fail {e}")
