from database.database import Database
from auth.security import hash_password 

def insert_user():
    db = Database()
    db.create_tables()

    utilisateurs = [
        {"nom": "merwan", "mot_de_passe": "mdp123"},
        {"nom": "thomas", "mot_de_passe": "123mdp"},
    ]

    for utilisateur in utilisateurs:
        nom = utilisateur["nom"]
        mot_de_passe_hash = hash_password(utilisateur["mot_de_passe"])
        user_id = db.add_user(nom, mot_de_passe_hash)

        if user_id:
            print(f"✅ Utilisateur '{nom}' créé avec succès ! ID : {user_id}")
        else:
            print(f"❌ Échec de la création de l'utilisateur '{nom}'.")

    db.close()

if __name__ == "__main__":
    insert_user()
