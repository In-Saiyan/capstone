import dotenv
import helpers.auth
import utils.db as db
import datetime
import helpers
# load conf from the .env file
dotenv.load_dotenv()

# make a connection to the database and login
dbcon = db.DatabaseConnection()


print("========================================")
# print(dbcon.fetch_table("user"))
# # print(dbcon.remove_record("user", "uid", "2"))
# print(dbcon.fetch_table("user"))

auth = helpers.auth.Auth()

dd = {
    "uname": "Shivansh Jain",
    "email": "axd@aec.com",
    "pno": "23664234543",
    "rdate":datetime.datetime.now().strftime("%Y-%m-%d"),
    "password":"Crazy"
}

dt = {
    "uname": "Yash Panchal",
    "email": "abd@aec.com",
    "pno": "23534234543",
    "rdate":datetime.datetime.now().strftime("%Y-%m-%d"),
    "password":"lmfao"
}

auth.register(dt)
auth.register(user_info=dd)
print(auth.login("abd@abc.com", "lmfao"))