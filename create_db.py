from connectdb import config_db
from psycopg2 import connect

params = config_db()
conn = connect(**params)
cur = conn.cursor()
# execute a statement
print('PostgreSQL database version:')
cur.execute('SELECT version()')
db_version = cur.fetchone()
print(db_version)

#def create_db():
#    con = connect
