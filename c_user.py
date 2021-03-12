import argparse
import models
from connectdb import config_db
from psycopg2 import connect
from passwords import check_password


params = config_db('database.ini', 'postgresql_comm')
conn = connect(**params)
conn.autocommit = True

parser = argparse.ArgumentParser()
parser.print_help()
#   u   p   n   d   e   l
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password")
parser.add_argument("-n", "--new_password", help="new password")
parser.add_argument("-d", "--delete", help="delete user", action="store_true")
parser.add_argument("-e", "--edit", help="edit user", action="store_true")
parser.add_argument("-l", "--list", help="list all users", action="store_true")

args = parser.parse_args()
print(args)


#nowy user -u -p
if args.username and args.password and args.new_password == None and not args.delete and not args.edit and not args.list :
    cur = conn.cursor()
    user = models.users.load_user_by_username(cur,str(args.username))
    if user:
        print(f"User {user.username} already exist")
    elif len(args.password) >= 8:
        new_user = models.users(args.username,args.password)
        if new_user.save_to_db(cur):
            print(f"User {args.username} added")
        else:
            print("Something went wrong")
    else:
        print("Password too short")
    

#nowe hasło -u -p -e -n
if args.username and args.password and args.new_password and not args.delete and args.edit and not args.list:
    if user and check_password(args.password,user.hashed_password):
        print('upen')

#usuwanie -u -p -d
if args.username and args.password and args.new_password == None and args.delete and not args.edit and not args.list:
    cur = conn.cursor()
    user = models.users.load_user_by_username(cur,str(args.username))
    if user and check_password(args.password,user.hashed_password):
        print(user.id)
        if user.delete_user(cur):
            print(f"User {args.username} deleted")
        else:
            print("Something went wrong")
    else:
        print("something went wrong")

#listowanie -l 
if args.username == None and args.password ==None and args.new_password == None and not args.delete and not args.edit and args.list:
    cur = conn.cursor()
    all = models.users.load_all_user(cur)
    for i in all:
        print(i.username)