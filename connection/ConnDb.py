from config import database

class Connection:

    def get_db(self):
        db = database.SessionLocal()
        try:
            yield db
        finally:
            db.close()