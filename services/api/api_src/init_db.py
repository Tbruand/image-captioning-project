from database.database import Database

def init_db():
    db = Database()
    db.create_tables()
    db.close()
    print("Base de données créée avec succès.")

if __name__ == "__main__":
    init_db()
