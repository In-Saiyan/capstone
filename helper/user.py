from ..utils.db import DatabaseCon
from ..utils import db

# # Dict structure
# dbcon.insert_record("user", {
#     "uid":"2",
#     "uname": "Shivansh Jain",
#     "email": "xyz@abc.com",
#     "pno": "0347809234",
#     "addr": "fjioawejfoweakfjawoef",
#     "rdate":datetime.datetime.now().strftime("%Y-%m-%d")
# })


class User:
    def __init__(self, con: DatabaseCon,uid: str, uname: str, email:str, pno: str, add: str, rdate):
        self.uid = uid
        self.uname = uname
        self.email = email
        self.pno = pno
        self.add = add
        self.rdate = rdate
        self.con = con
        


