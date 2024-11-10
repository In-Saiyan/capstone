import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

TABLES = {
    'user': (
        "CREATE TABLE IF NOT EXISTS user ("
        "  uid VARCHAR(16) PRIMARY KEY NOT NULL,"
        "  uname VARCHAR(40) NOT NULL,"
        "  email VARCHAR(60) UNIQUE NOT NULL,"
        "  pno VARCHAR(14) NOT NULL,"
        "  addr VARCHAR(80) NOT NULL,"
        "  rdate DATE NOT NULL"
        ")"),
    'product': (
        "CREATE TABLE IF NOT EXISTS product ("
        "  pid VARCHAR(36) PRIMARY KEY NOT NULL,"
        "  pname VARCHAR(50) NOT NULL,"
        "  cid VARCHAR(16) NOT NULL,"
        "  price INT NOT NULL,"
        "  stock INT NOT NULL,"
        "  adate DATE NOT NULL,"
        "  imgurl VARCHAR(50)"
        ")"),
    'orders': (
        "CREATE TABLE IF NOT EXISTS orders ("
        "  oid VARCHAR(36) PRIMARY KEY NOT NULL,"
        "  uid VARCHAR(16) NOT NULL,"
        "  pid VARCHAR(36) NOT NULL,"
        "  odate DATE NOT NULL,"
        "  qty INT NOT NULL,"
        "  tprice INT NOT NULL"
        ")"),
    'reviews': (
        "CREATE TABLE IF NOT EXISTS reviews ("
        "  rid VARCHAR(36) PRIMARY KEY NOT NULL,"
        "  uid VARCHAR(16) NOT NULL,"
        "  pid VARCHAR(36) NOT NULL,"
        "  rating INT NOT NULL,"
        "  rtext TEXT,"
        "  rdate DATE NOT NULL"
        ")"),
    'category': (
        "CREATE TABLE IF NOT EXISTS category ("
        "  cid VARCHAR(16) PRIMARY KEY NOT NULL,"
        "  cname VARCHAR(30),"
        "  cdesc TEXT,"
        "  isactive BOOL NOT NULL"
        ")"),
    'cart': (
        "CREATE TABLE IF NOT EXISTS cart ("
        "  crt_id VARCHAR(16) PRIMARY KEY NOT NULL,"
        "  uid VARCHAR(16) NOT NULL,"
        "  pid VARCHAR(36) NOT NULL,"
        "  qty INT NOT NULL,"
        "  price INT NOT NULL,"
        "  adate DATE NOT NULL,"
        "  FOREIGN KEY (uid) REFERENCES user(uid),"
        "  FOREIGN KEY (pid) REFERENCES product(pid)"
        ")"),
    'shipping_address': (
        "CREATE TABLE IF NOT EXISTS shipping_address ("
        "  said VARCHAR(36) PRIMARY KEY,"
        "  uid VARCHAR(16) NOT NULL,"
        "  STREET VARCHAR(40),"
        "  CITY VARCHAR(30) NOT NULL,"
        "  STATE VARCHAR(30) NOT NULL,"
        "  POSTALCODE VARCHAR(10) NOT NULL,"
        "  FOREIGN KEY (uid) REFERENCES user(uid)"
        ")"),
    'paymentmethod': (
        "CREATE TABLE IF NOT EXISTS paymentmethod ("
        "  PAYID VARCHAR(16) PRIMARY KEY,"
        "  UID VARCHAR(16) NOT NULL,"
        "  PTYPE VARCHAR(36) NOT NULL,"
        "  PTID INT NOT NULL,"
        "  IDNO VARCHAR(30) NOT NULL,"
        "  EXDATE DATE NOT NULL,"
        "  BillingZip VARCHAR(10) NOT NULL,"
        "  FOREIGN KEY (UID) REFERENCES user(UID)"
        ")"),
    'user_passwords': (
        "CREATE TABLE IF NOT EXISTS user_passwords ("
        "  uid VARCHAR(16) PRIMARY KEY NOT NULL,"
        "  hashed_password VARCHAR(100)"
        ")")
}

def create_database(cursor):
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} DEFAULT CHARACTER SET 'utf8'")

def create_tables(cursor):
    cursor.execute(f"USE {DB_NAME}")
    for table_name, table_description in TABLES.items():
        cursor.execute(table_description)
        print(f"Table `{table_name}` created successfully.")

def describe_tables(cursor):
    cursor.execute(f"USE {DB_NAME}")
    for table_name in TABLES.keys():
        print(f"\nDescription of `{table_name}` table:")
        cursor.execute(f"DESCRIBE {table_name}")
        for row in cursor.fetchall():
            print(row)

try:
    cnx = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        charset='utf8mb4'
    )
    cursor = cnx.cursor()


    create_database(cursor)
    cnx.select_db(DB_NAME)
    create_tables(cursor)
    describe_tables(cursor)

    cnx.commit()

finally:
    cursor.close()
    cnx.close()
