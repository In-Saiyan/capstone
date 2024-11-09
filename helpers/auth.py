import os
import jwt
import bcrypt
from datetime import datetime, timedelta
from utils.db import DatabaseConnection
import hashlib

# tokenization and password hash-generation from online sites
# bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
# jwt.encode({'uid': uid, 'exp': expiration}, self.secret_key, algorithm='HS256')

class Auth:
    def __init__(self):
        self.db = DatabaseConnection()
        self.secret_key = os.getenv("SECRET_KEY", "your_secret_key")  # Replace with a secure key

    def register(self, user_info: dict) -> str:
        """
        Register a new user using a dictionary of user info.

        Args:
            user_info (dict): A dictionary containing user information with keys:
                              'uname', 'email', 'pno', 'addr', and 'password'.

        Returns:
            str: Result message.
        """
        uid = self._generate_uid(user_info['email'])  # Generate a unique user ID
        hashed_password = bcrypt.hashpw(user_info['password'].encode('utf-8'), bcrypt.gensalt())

        # User data to insert into the user table
        user_data = {
            'uid': uid,
            'uname': user_info['uname'],
            'email': user_info['email'],
            'pno': user_info['pno'],
            'addr': user_info['addr'],
            'rdate': datetime.now().date()
        }

        # Insert user into the user table
        insert_response = self.db.insert_record('user', user_data)

        if insert_response == "Record inserted successfully":
            # Insert hashed password into the user_passwords table
            password_data = {
                'uid': uid,
                'hashed_password': hashed_password.decode('utf-8')
            }
            insert_password_response = self.db.insert_record('user_passwords', password_data)

            if insert_password_response == "Record inserted successfully":
                return "User registered successfully"
            else:
                # Roll back the user creation if password insertion fails
                self.db.remove_record('user', 'uid', uid)
                return insert_password_response
        return insert_response

    def _generate_uid(self, email: str) -> str:
        """
        Generate a unique user ID.
        
        Returns:
            str: Unique user ID.
        """
        return hashlib.sha256(email.encode()).hexdigest()[:16]

    def login(self, email: str, password: str) -> str:
        """
        Login a user and return a JWT token.

        Args:
            email (str): User's email.
            password (str): User's password.

        Returns:
            str: JWT token if successful, otherwise error message.
        """
        user = self.db.fetch_row('user', 'email', email)

        if not user:
            return "User not found"

        uid = user[0][0]  # Assuming uid is the first column
        hashed_password = self.db.fetch_row('user_passwords', 'uid', uid)[0][1]

        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            token = self._generate_token(uid)
            return token
        return "Invalid password"


    def _generate_token(self, uid: str) -> str:
        """
        Generate a JWT token.

        Args:
            uid (str): User ID to encode in the token.

        Returns:
            str: JWT token.
        """
        expiration = datetime.utcnow() + timedelta(hours=2)  # Token valid for 2 hours
        token = jwt.encode({'uid': uid, 'exp': expiration}, self.secret_key, algorithm='HS256')
        return token

    def verify_token(self, token: str) -> dict:
        """
        Verify the JWT token.

        Args:
            token (str): JWT token to verify.

        Returns:
            dict: Decoded token data if valid, otherwise None.
        """
        try:
            decoded = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return decoded
        except jwt.ExpiredSignatureError:
            return {"error": "Token has expired"}
        except jwt.InvalidTokenError:
            return {"error": "Invalid token"}
