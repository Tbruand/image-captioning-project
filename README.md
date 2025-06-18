# 🧠 Image Captioning Project

Projet de génération automatique de légendes à partir d’images.
Conçu dans un cadre pédagogique, il suit une approche **MLOps** et **microservices**.

---

## 📦 Objectifs

* 🎯 Construire un modèle Deep Learning (CNN + RNN) pour le captioning d’images
* 🧪 Suivre les expériences et les métriques avec MLflow
* ⚙️ Servir le modèle via une API REST (FastAPI)
* 🖼️ Fournir une interface web simple (Gradio ou autre)
* 🚀 Structurer le projet en microservices pour faciliter le développement et le déploiement

---

## 🗂️ Arborescence du projet

```bash
.
├── data/                  # Données brutes et prétraitées (README inclus)
├── docker-compose.yml     # Orchestration des services
├── docs/                  # Documentation interne (conventions Git, etc.)
├── mlflow/                # Tracking des expériences (README, mlruns/)
├── models/                # Modèles enregistrés (README, fichiers ignorés)
├── README.md              # 👉 Ce fichier
├── requirements.txt       # Dépendances globales
├── services/              # Microservices
│   ├── api/               # Backend (FastAPI/Flask)
│   ├── frontend/          # Interface utilisateur (ex: Gradio)
│   └── training/          # Scripts d'entraînement
└── venv/                  # Environnement virtuel local (non suivi)
```

---

## ⚙️ Installation rapide

```bash
# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate.bat # Windows

# Installer les dépendances
pip install -r requirements.txt
```

---

## 🧪 Lancer les services

> ⚠️ WIP


---

## 🧰 Conventions de développement

Consultez le fichier 👉 [`docs/CONVENTIONS_GIT.md`](docs/CONVENTIONS_GIT.md)

* Structure Git avec `main`, `dev`, `prod`
* Commits normalisés (style Commitizen)
* Pull Requests obligatoires avec template
* MLflow à venir pour le suivi des expériences

---

## 🛣️ Roadmap

* [x] Initialisation du projet
* [x] Structuration des dossiers
* [x] Mise en place des conventions Git
* [ ] Prétraitement des données
* [ ] Entraînement du modèle
* [ ] Intégration API
* [ ] Interface web
* [ ] Déploiement final

---

## 👥 Auteurs

* **Thomas** – GitHub manager, architecture & CI
* **Merwan** – Binôme Dev & intégration
