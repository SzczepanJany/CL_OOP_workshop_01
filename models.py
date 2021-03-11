from hashlib import new
from connectdb import config_db
from psycopg2 import connect, errors
from passwords import hash_password

params = config_db('database.ini', 'postgresql_comm')
conn = connect(**params)
conn.autocommit = True

class users():

    @staticmethod
    def load_user_by_id(cursor, id_):
        sql="""select id, username, hashed_password from users where id=%s"""
        cursor.execute(sql, (id_,))
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = users(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user
        else:
            return None 

    @staticmethod
    def load_user_by_username(cursor, username):
        sql="""select id, username, hashed_password from users where username=%s"""
        cursor.execute(sql, (username,))
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = users(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user
        else:
            return None 

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
            sql = """insert into users (username, hashed_password) values (%s, %s) returning id"""
            values = (self.username, self.hashed_password)
            cursor.execute(sql,values)
            self._id = cursor.fetchone()[0]
            return True
        return False
    


new_user = users('johny', 'tratata')
cur = conn.cursor()
new_user.save_to_db(cur)
print(users.load_user_by_id(cur, 4))
print(users.load_user_by_username(cur, 'johny'))

print(users.load_user_by_id(cur, 2))
print(users.load_user_by_username(cur, 'jony'))