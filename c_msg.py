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
#   u   p   t   s   l
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password")
parser.add_argument("-t", "--to", help="send to user")
parser.add_argument("-s", "--send", help="test to send in a message")
parser.add_argument("-l", "--list", help="list all users", action="store_true")

args = parser.parse_args()
print(args)


#przeczytaj wiadomości -u -p -l
if args.username and args.password and not args.to and args.list and not args.send:
    cur = conn.cursor()
    user = models.users.load_user_by_username(cur,str(args.username))
    if user and check_password(args.password,user.hashed_password):
        msg = models.messages.load_all_messages_to(cur, user.id)
        for i in msg:
            print(f"User {i.from_id} send a message: {i.m_text}; on {i.creation_date}")
    else:
        print("User not authorise")
    

#nowe hasło -u -p -s -t
if args.username and args.password and args.to and not args.list and args.send:
    cur = conn.cursor()
    user = models.users.load_user_by_username(cur,str(args.username))
    if user and check_password(args.password,user.hashed_password):
        user_to = models.users.load_user_by_username(cur,str(args.to))
        if user_to:
            msg = models.messages(args.send, user.id, user_to.id)
            if msg.save_to_db(cur):
                print("Message sent")
            else:
                print("Something went wrong")
        else:
            print("User not authorise")
    else:
        print("Something went wrong")    

