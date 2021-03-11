from connectdb import config_db
from psycopg2 import connect, errors
from passwords import hash_password

params = config_db('database.ini', 'postgresql_comm')
conn = connect(**params)
conn.autocommit = True

class users():
    def __init__(self, username='', password='', salt=''):
        self._id = -1
        self.username = username
        #po co to tu skoro jest setter?
        self._hashed_password = hash_password(password, salt)

    @property
    def id(self):
        return self._id

    @property
    def hashed_password(self):
        return self._hashed_password

    def set_password(self, password, salt=''):
        self._hashed_password = hash_password(password, salt)
    
    @hashed_password.setter
    def hashed_password(self, password):
        self.set_password(password)

    def save_to_db(self, cursor):
        if self._id == -1:
            sql = """insert into users values (username, hased_password) values (%s, %s) returning id"""
            values = (self.username, self.hashed_password)
            cursor.execute(sql,values)
            self._id = cursor.fetchone()['id']
            return True
        return False
    