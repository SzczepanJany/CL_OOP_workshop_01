from hashlib import new
from connectdb import config_db
from psycopg2 import connect, errors
from passwords import hash_password
from datetime import datetime

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
        sql="""select id, m_text, from_id, to_id, creation_date from messages """
        cursor.execute(sql)
        all_message = []
        data = cursor.fetchall()
        for row in data:
            id_, m_text, from_id, to_id, creation_date = row
            loaded_message = messages()
            loaded_message._id = id_
            loaded_message.m_text = m_text
            loaded_message.from_id = from_id
            loaded_message.to_id = to_id
            loaded_message.creation_date = creation_date
            all_message.append(loaded_message)
        return all_message
        
    def __init__(self, m_text='', from_id='', to_id=''):
        self._id = -1
        self.m_text = m_text 
        self.from_id = from_id
        self.to_id = to_id
        self.creation_date = None

    @property
    def id(self):
        return self._id

    def save_to_db(self, cursor):
        if self._id == -1:
            sql = """insert into messages (m_text, from_id, to_id, creation_date) values (%s, %s, %s, %s) returning id"""
            values = (self.m_text, self.from_id, self.to_id, datetime.now())
            cursor.execute(sql,values)
            self._id = cursor.fetchone()[0]
            return True
        else:
            #czy napewno potrzeba update?
            sql = """ update messages set m_text=%s, to_id=%s where id=%s"""
            values = (self.usernamem_text, self.to_id, self.id)
            cursor.execute(sql,values)
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

new_message1 = messages('test1', 32, 36)
new_message2 = messages('test', 32, 37)
new_message1.save_to_db(cur)
new_message2.save_to_db(cur)
all_m=messages.load_all_messages(cur)
for i in all_m:
    print(i.m_text,i.from_id,i.to_id,i.creation_date)
