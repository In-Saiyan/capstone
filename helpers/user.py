from utils.db import DatabaseConnection

class UserManager:
    def __init__(self, db: DatabaseConnection = None):
        
        self.db = DatabaseConnection() if not db else db

    def create_user(self, uid, uname, email, pno, addr, rdate):
        data = {
            "uid": uid,
            "uname": uname,
            "email": email,
            "pno": pno,
            # "addr": addr,
            "rdate": rdate
        }
        return self.db.insert_record("user", data)

    def get_user_by_id(self, uid):
        return self.db.fetch_row("user", "uid", uid)

    def update_user(self, uid, updates):
        return self.db.update_record("user", updates, "uid", uid)

    def delete_user(self, uid):
        return self.db.remove_record("user", "uid", uid)
