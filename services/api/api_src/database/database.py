import sqlite3
import pytz
from datetime import datetime
import os

DB_FILE = os.path.join(os.path.dirname(__file__), 'database.db')

class Database:
    def __init__(self):
        try:
            self.conn = sqlite3.connect(DB_FILE, check_same_thread=False)
            self.conn.execute("PRAGMA foreign_keys = ON;")
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Erreur de connexion à la base : {e}")
            self.conn = None
            self.cursor = None

    
    def _get_local_now(self):
        paris_tz = pytz.timezone("Europe/Paris")
        return datetime.now(paris_tz).strftime("%Y-%m-%d %H:%M:%S")

    def create_tables(self):
        if not self.conn:
            print("Pas de connexion.")
            return
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS User (
                    id_user INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom_user VARCHAR(50) NOT NULL,
                    mdp_user VARCHAR(255) NOT NULL,
                    date_creation TIMESTAMP NOT NULL
                );
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Image (
                    id_image INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom_fichier VARCHAR(255) NOT NULL,
                    date_fichier TIMESTAMP NOT NULL,
                    id_user INTEGER NOT NULL,
                    FOREIGN KEY (id_user) REFERENCES User(id_user) ON DELETE CASCADE
                );
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Prediction (
                    id_pred INTEGER PRIMARY KEY AUTOINCREMENT,
                    resultat_pred VARCHAR(200) NOT NULL,
                    confiance_pred FLOAT NOT NULL,
                    monitor_pred INTEGER NOT NULL,
                    date_pred TIMESTAMP NOT NULL,
                    id_image INTEGER NOT NULL UNIQUE,
                    FOREIGN KEY (id_image) REFERENCES Image(id_image) ON DELETE CASCADE
                );
            """)
            self.conn.commit()
            print("Tables créées ou déjà existantes.")
        except sqlite3.Error as e:
            print(f"Erreur de création des tables : {e}")

    def get_connection(self):
        return self.conn

    def close(self):
        if self.conn:
            self.conn.close()

    def add_user(self, nom_user: str, mdp_user: str) -> int | None:

        try:
            # Ici, plus tard, tu feras : mdp_user = hash_password(mdp_user)
            now_local = self._get_local_now()
            self.cursor.execute("""
                INSERT INTO User (nom_user, mdp_user, date_creation)
                VALUES (?, ?, ?)
            """, (nom_user, mdp_user, now_local))
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            print(f"Erreur lors de l'insertion d'un utilisateur : {e}")
            return None
