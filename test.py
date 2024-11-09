import dotenv
import helpers.auth
import utils.db as db
import datetime
import helpers
# load conf from the .env file
dotenv.load_dotenv()

# make a connection to the database and login
dbcon = db.DatabaseConnection()

res = dbcon.fetch_row("user", "uid", "1")
i = dbcon.insert_record("user", {
    "uid":"2",
    "uname": "Shivansh Jain",
    "email": "xyz@abc.com",
    "pno": "043623656",
    "addr": "fjioawejfoweakfjawoef",
    "rdate":datetime.datetime.now().strftime("%Y-%m-%d")
})
res2 = dbcon.fetch_row("user", "uid", "2")
print(res)
print(i)
print(res2)
print(dbcon.update_record("user", {
    "uid":"2",
    "uname": "Shivansh Jain",
    "email": "xyz@abc.com",
    "pno": "23524543",
    "addr": "fjioawejfoweakfjawoef",
    "rdate":datetime.datetime.now().strftime("%Y-%m-%d")
}))
res2 = dbcon.fetch_row("user", "uid", "2")
print(res2)
print("========================================")
print(dbcon.fetch_table("user"))
print(dbcon.remove_record("user", "uid", "2"))
print(dbcon.fetch_table("user"))

auth = helpers.auth.Auth()

dt = {
    "uid":"4",
    "uname": "Harshit Vaish",
    "email": "abd@abc.com",
    "pno": "23534234543",
    "addr": "Jabalpur, MP",
    "rdate":datetime.datetime.now().strftime("%Y-%m-%d"),
    "password":"lmfao"
}

auth.register(dt)
print(auth.login("abd@abc.com", "lmfao"))