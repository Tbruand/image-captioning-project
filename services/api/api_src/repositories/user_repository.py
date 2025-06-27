from api_src.database.database import Database

class UserRepository:
    def __init__(self, db: Database):
        self.db = db

    def get_password_hash_by_username(self, nom_user: str) -> str | None:
        query = "SELECT mdp_user FROM User WHERE nom_user = ?"
        self.db.cursor.execute(query, (nom_user,))
        row = self.db.cursor.fetchone()
        if row:
            return row[0]
        return None
    
    def get_id_by_username(self, username: str) -> int | None:
        self.db.cursor.execute(
            "SELECT id_user FROM User WHERE nom_user = ?",
            (username,)
        )
        result = self.db.cursor.fetchone()
        if result:
            return result[0]  # id
        return None