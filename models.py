from hashlib import new
from connectdb import config_db
from psycopg2 import connect, errors
from passwords import hash_password

params = config_db('database.ini', 'postgresql_comm')
conn = connect(**params)
conn.autocommit = True

class users():

    @staticmethod
    def load_all_user(cursor):
        sql="""select id, username, hashed_password from users """
        cursor.execute(sql)
        all_users = []
        data = cursor.fetchall()
        for row in data:
            id_, username, hashed_password = row
            loaded_user = users()
            loaded_user.username = username
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            all_users.append(loaded_user)
        return all_users
        
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
        else:
            sql = """ update users set username=%s, hashed_password=%s where id=%s"""
            values = (self.username, self.hashed_password, self.id)
            cursor.execute(sql,values)
            return True
        return False
    
    def delete_user(self, cursor):
        if self._id == -1:
            sql=""" delete from users where id=%s"""
            cursor.execute(sql,(self.id,))
            self._id = -1
            return True
        return False



class messages():

    @staticmethod
    def load_all_messages(cursor):
        sql="""select id, m_text, from_id, to_id from users """
        cursor.execute(sql)
        all_users = []
        data = cursor.fetchall()
        for row in data:
            id_, username, hashed_password = row
            loaded_user = users()
            loaded_user.username = username
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            all_users.append(loaded_user)
        return all_users
        
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
        else:
            sql = """ update users set username=%s, hashed_password=%s where id=%s"""
            values = (self.username, self.hashed_password, self.id)
            cursor.execute(sql,values)
            return True
        return False
    
    def delete_user(self, cursor):
        if self._id == -1:
            sql=""" delete from users where id=%s"""
            cursor.execute(sql,(self.id,))
            self._id = -1
            return True
        return False



cur = conn.cursor()
new_user = users('johny', 'tratata')
new_user1 = users('johana', 'trututu')
new_user.save_to_db(cur)
new_user1.save_to_db(cur)
print(users.load_user_by_id(cur, 4))
old_user = users.load_user_by_id(cur, 34)
print(old_user)
old_user.username = 'sara'
old_user.save_to_db(cur)
print(users.load_user_by_id(cur, 2))
print(users.load_user_by_username(cur, 'jony'))



all = users.load_all_user(cur)
for i in all:
    print(i.id, i.username)