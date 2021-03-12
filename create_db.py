from connectdb import config_db
from psycopg2 import connect, errors

params = config_db()
conn = connect(**params)
conn.autocommit = True

def conn_test():
    cur = conn.cursor()
    # execute a statement
    print('PostgreSQL database version:')
    cur.execute('SELECT version()')
    db_version = cur.fetchone()
    print(db_version)
    cur.close()

def create_db():
    cur = conn.cursor()
    try:
        cur.execute('create database communicates')
    except errors.DuplicateDatabase:
        print("Database 'communicates' already exist")

    cur.close()
    conn.close()


def create_table_users():
    cur = conn.cursor()
    try:
        cur.execute('create table users(id serial not null, username varchar(255) unique,hashed_password varchar(80) not null, primary key(id))')
    except errors.DuplicateTable:
        print("Table 'users' already exist")
    cur.close()

def create_table_messages():
    cur = conn.cursor()
    try:
        cur.execute('create table messages(id serial not null, m_text text not null, from_id int not null, to_id int not null, creation_date TIMESTAMP not null default now(), primary key(id), foreign key(from_id) references users(id) ON DELETE CASCADE, foreign key(to_id) references users(id) ON DELETE CASCADE)')
    except errors.DuplicateTable:
        print("Table 'messages' already exist")
    cur.close()

create_db()
params = config_db('database.ini', 'postgresql_comm')
conn = connect(**params)
conn.autocommit = True

create_table_users()
create_table_messages()