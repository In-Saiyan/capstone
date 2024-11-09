import dotenv
import utils.db as db
import datetime
# load conf from the .env file
dotenv.load_dotenv()

# make a connection to the database and login
dbcon = db.DatabaseCon()

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
dbcon.update_record("user", {
    "uid":"2",
    "uname": "Shivansh Jain",
    "email": "xyz@abc.com",
    "pno": "23524543",
    "addr": "fjioawejfoweakfjawoef",
    "rdate":datetime.datetime.now().strftime("%Y-%m-%d")
})
res2 = dbcon.fetch_row("user", "uid", "2")
print(res2)