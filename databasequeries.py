class DatabaseQueries:
    """
    Database queries for DatabaseConnector
    PostgreSQL
    Database schema.jpg and dump file included
    """
    ALL_DRINKS = """
            SELECT id, drink FROM drinks
            """

    AVAILABLE_DRINKS = """
            SELECT DISTINCT drink FROM drinks
            JOIN recipes ON drinks.id = recipes.drink_id
            JOIN ingredients ON recipes.ingredient_id = ingredients.id
            LEFT JOIN pumps ON ingredients.id = pumps.ingredient_id
            WHERE drink_id IN (
                SELECT drink_id FROM drinks
                JOIN recipes ON drinks.id = recipes.drink_id
                JOIN ingredients ON recipes.ingredient_id = ingredients.id
                LEFT JOIN pumps ON ingredients.id = pumps.ingredient_id
                GROUP BY 1
                HAVING bool_and(pumps.id IS NOT NULL)
            )
            """

    AVAILABLE_RECIPE = """
            SELECT pumps.id, quantity FROM drinks
            JOIN recipes ON drinks.id = recipes.drink_id
            JOIN ingredients ON recipes.ingredient_id = ingredients.id
            JOIN pumps ON pumps.ingredient_id = ingredients.id
            WHERE drink=%s
            """

    RECIPE = """
            SELECT recipes.id, drinks.id, ingredients.id, quantity, drinks.drink, ingredients.ingredient FROM drinks
            JOIN recipes ON drinks.id = recipes.drink_id
            JOIN ingredients ON recipes.ingredient_id = ingredients.id
            WHERE drink=%s
            """

    ALL_RECIPES = """
            SELECT drinks.id, drinks.drink, ingredients.id, ingredients.ingredient, quantity FROM drinks
            JOIN recipes ON drinks.id = recipes.drink_id
            JOIN ingredients ON recipes.ingredient_id = ingredients.id
            """

    ALL_INGREDIENTS = """
            SELECT * FROM ingredients
            """

    INSERT_RECIPE = """
                INSERT INTO recipes (drink_id, ingredient_id, quantity)
                VALUES (%s,%s,%s)
                """

    INSERT_DRINK = """
                INSERT INTO drinks (drink)
                VALUES (%s)
                """

    CREATE_USER = """
            INSERT INTO users (name, face, img, admin)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (id)
            DO UPDATE SET name=EXCLUDED.name, face=EXCLUDED.face, img=EXCLUDED.img
            """

    USERS_FACES = """
            SELECT * FROM users
            """

    USERS_NAMES = """
            SELECT name FROM users
            """

    USER_IS_ADMIN = """
            SELECT admin FROM users
            WHERE name=%s
            """

    USERS = """
            SELECT id, name, img FROM users
            """

    USER_IMG = """
            SELECT img FROM users
            WHERE name=%s
            """

    USER_HISTORY = """
            SELECT drinks.drink, timestamp FROM orders
            JOIN users on users.id = orders.user_id
            JOIN drinks on drinks.id = orders.drink_id
            WHERE users.name=%s
            """

    DELETE_USER = """
            DELETE FROM users
            WHERE id=%s
            """

    GET_PUMPS_INGREDIENTS = """
            SELECT pumps.id, ingredients.id, ingredients.ingredient FROM pumps
            LEFT JOIN ingredients on pumps.ingredient_id = ingredients.id
            """

    SET_PUMP_INGREDIENTS = """
            INSERT INTO pumps (id, ingredient_id)
            VALUES (%s, (NULLIF(%s,'None')::integer))
            ON CONFLICT (id) DO UPDATE SET id = EXCLUDED.id, ingredient_id = EXCLUDED.ingredient_id
            """

    ORDER = """
            INSERT INTO orders (user_id, drink_id, timestamp)
            VALUES (%s, %s, %s)
            """

    GET_DRINK_ID = """
            SELECT drinks.id FROM drinks
            WHERE drink=%s
            """

    GET_USER_INFO = """
            SELECT id, name, img, admin FROM users
            WHERE name=%s
            """

    DRINK_EXISTS = """
            SELECT drink FROM drinks WHERE drink = %s;
    """

    DELETE_RECIPE = """
            DELETE FROM recipes WHERE drink_id = %s;
            """

    GET_INGREDIENT_ID = """
            SELECT id FROM ingredients WHERE ingredient = %s;
    """