# 📚 Notebooks - Image Captioning Project (CNN + LSTM + Attention)

Cette section contient les notebooks Jupyter utilisés pour explorer, prétraiter, entraîner et évaluer notre modèle de génération de légendes à partir d'images sur le dataset **Flickr8k**.

---

## 🗂️ Structure des Notebooks

| Notebook | Description |
|---------|-------------|
| `01_eda_image.ipynb` | 🔍 Analyse exploratoire des images : dimensions, canaux, formats, distribution, échantillons visuels. |
| `01_eda_text.ipynb` | 🔍 Analyse exploratoire des descriptions textuelles : longueur des phrases, vocabulaire, fréquence des mots. |
| `02_augmentation.ipynb` | 📸 Génération d’images augmentées (rotation, crop, flip, etc.) pour renforcer la robustesse du modèle. |
| `03_prepocessing.ipynb` | 🧼 Prétraitement des données : redimensionnement des images, extraction de features via ResNet, nettoyage des textes. |
| `04_vocab_building.ipynb` | 🧠 Construction du vocabulaire et tokenisation avec ajout des tokens spéciaux `<start>`, `<end>`, `<pad>`, `<unk>`. |
| `05_dataset_and_dataloader.ipynb` | 🧱 Construction du Dataset PyTorch personnalisé et du DataLoader pour l’entraînement. |
| `06_training.ipynb` | 🏋️ Entraînement du modèle CNN + LSTM avec attention, métriques BLEU-3 et ROUGE-L, early stopping, sauvegardes. |
| `07_inference.ipynb` | 📷 Génération de légendes à partir d’images avec un modèle entraîné (mode évaluation/inférence). |


---

## 📦 Objectif global

Ce dossier vise à construire pas à pas un pipeline complet de **Image Captioning**, incluant :
- Préparation et augmentation des données,
- Construction du vocabulaire,
- Entraînement du modèle avec attention,
- Évaluation via des métriques classiques,
- Inférence et visualisation des résultats.

---

## 💡 À noter

- Tous les notebooks sont modulaires et suivent l’ordre recommandé d’exécution.
- Le projet respecte une approche **orientée objet** et prépare les composants pour une intégration API.

---

## 🧪 Prochaines étapes

- ✅ Intégration continue des notebooks dans un pipeline d’entraînement complet.
- 🔄 Ajout d’un notebook `08_metrics_analysis.ipynb` (optionnel) pour visualiser les courbes de perte, BLEU/ROUGE dans le temps.
- 🚀 Déploiement API + Interface utilisateur (voir dossier `api/` et `frontend/`).

---

## 👥 Auteurs

Projet réalisé par **Thomas** et **Merwan** dans le cadre de notre formation en IA.  
Méthodologie agile (Scrum / Scrumban), GitHub conventionné (Commitizen), CI/CD prévu.

---