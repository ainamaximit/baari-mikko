import psycopg2
conn = psycopg2.connect("host=localhost dbname=test1 user=mikko password=baari")
cur = conn.cursor()
with open('recipes.csv', 'r') as f:
    # Notice that we don't need the `csv` module.
    next(f) # Skip the header row.
    cur.copy_from(f, 'recipes', sep=',')

conn.commit()
print("updated")