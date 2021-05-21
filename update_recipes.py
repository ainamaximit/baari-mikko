import psycopg2
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

conn = psycopg2.connect(
                database=config.get('DATABASE', 'database'),
                user=config.get('DATABASE', 'username'),
                password=config.get('DATABASE', 'password'),
                host=config.get('DATABASE', 'ip_address'),
            )
cur = conn.cursor()
with open(config.get('BAARIMIKKO', 'recipes'), 'r') as f:

    next(f)  # Skip the header row.
    cur.copy_from(f, 'recipes', sep=',')

conn.commit()
print("updated")
