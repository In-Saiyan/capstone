import dotenv
import utils.db as db

# load conf from the .env file
dotenv.load_dotenv()

# make a connection to the database and login
dbcon = db.DatabaseCon()

