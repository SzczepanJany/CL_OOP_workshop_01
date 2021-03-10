from psycopg2 import connect
from connect_db import config

params = config()
conn = connect(**params)
cur = conn.cursor()
# execute a statement
print('PostgreSQL database version:')
cur.execute('SELECT version()')


#def create_db():
#    con = connect