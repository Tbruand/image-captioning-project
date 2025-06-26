from sqlite3 import IntegrityError
from api_src.database.database import Database

class ImageRepository:
    def __init__(self, db: Database):
        self.db = db

    def add_image(self, nom_fichier: str, id_user: int) -> int | None:
        try:
            now_local = self.db._get_local_now()
            self.db.cursor.execute(
                "INSERT INTO Image (nom_fichier, date_fichier, id_user) VALUES (?, ?, ?)",
                (nom_fichier, now_local, id_user)
            )
            self.db.conn.commit()
            return self.db.cursor.lastrowid
        except IntegrityError as e:
            print(f"Erreur de clé étrangère (id_user invalide ?) : {e}")
            return None
        except Exception as e:
            print(f"Erreur lors de l'insertion d'une image : {e}")
            return None
    
    def add_prediction(self, resultat_pred: str, confiance_pred: float, id_image: int, monitor_pred: int = 0) -> int | None:
        try:
            now_local = self.db._get_local_now()
            self.db.cursor.execute(
                "INSERT INTO Prediction (resultat_pred, confiance_pred, monitor_pred, date_pred, id_image) VALUES (?, ?, ?, ?, ?)",
                (resultat_pred, confiance_pred, monitor_pred, now_local, id_image)
            )
            self.db.conn.commit()
            return self.db.cursor.lastrowid
        except Exception as e:
            print(f"Erreur lors de l'insertion d'une prédiction : {e}")
            return None
        
    def update_monitor_pred(self, id_image: int, monitor_pred: int) -> bool:
        try:
            self.db.cursor.execute(
                "UPDATE Prediction SET monitor_pred = ? WHERE id_image = ?",
                (monitor_pred, id_image)
            )
            self.db.conn.commit()
            return True
        except Exception as e:
            print(f"Erreur lors de la mise à jour du feedback : {e}")
            return False
