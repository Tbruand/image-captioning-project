# 📚 Conventions Git du Projet (Thomas / Merwan)

## 🔧 Structure des branches

### 🌿 Branches principales

* `main` : Contient une version stable et validée du projet. Elle n'accueille que des Pull Requests depuis `dev`.
* `dev` : Branche de développement. Toutes les nouvelles fonctionnalités sont mergées ici.
* `prod` : Branche de production, protégée. Mise à jour uniquement via PR depuis `main`.

### 🔀 Branches de fonctionnalité (microservices)

* Créer depuis `dev`
* Nommage : `<type>/<nom-du-service>`

Exemples :

* `feat/nlp-service`
* `fix/api-token`
* `docs/architecture`

---

## ✍️ Convention de commit (style Commitizen, sans librairie)

### 🧱 Format

```bash
<type>(scope): message clair et concis
```

### 🔠 Types acceptés

| Type     | Description                          |
| -------- | ------------------------------------ |
| feat     | Nouvelle fonctionnalité              |
| fix      | Correction de bug                    |
| docs     | Documentation                        |
| style    | Formatage / indentation              |
| refactor | Refacto sans ajout de fonctionnalité |
| test     | Ajout ou modification de tests       |
| chore    | Tâches annexes (CI, dépendances)     |
| perf     | Amélioration des performances        |

### ✅ Exemples

```bash
feat(api): ajout de la route /predict
fix(auth): correction du bug de token expiré
docs(readme): ajout de la roadmap initiale
```

---

## 🚀 Pull Requests

### 🔁 Règles générales

* Toujours faire une PR pour fusionner dans `dev`, `main` ou `prod`
* Aucune fusion directe via `git merge` sans revue (sauf urgence)
* Toujours partir de la dernière version de la branche cible

### 📄 Template `.github/pull_request_template.md`

```md
# 🚀 Pull Request – [Nom de la feature ou fix]

## 📌 Description
<!-- Décrivez en quelques lignes ce que contient cette PR -->

## 🔍 Liée à
<!-- Indiquez les issues ou cartes Trello associées -->

## ✅ Checklist
- [ ] Le code compile et fonctionne
- [ ] Les tests passent (quand il y en aura)
- [ ] La PR est bien vers `dev`
- [ ] J’ai relu mon code
- [ ] J’ai respecté la convention de commit

## 📸 Captures ou Démo (si applicable)
<!-- Ajoutez un screenshot ou un lien Gradio/FastAPI/etc. -->
```

---

## 🧰 Commandes Git à connaître

### 🔨 Initialisation du repo

```bash
git init
git checkout -b main
git commit --allow-empty -m "chore(init): initial commit with main branch"
git push -u origin main
git checkout -b dev
git push -u origin dev
git checkout -b prod
git push -u origin prod
```

### 🌱 Créer une branche de fonctionnalité

```bash
git checkout dev
git pull origin dev
git checkout -b feat/nlp-service
```

### ✅ Commit structuré

```bash
git add .
git commit -m "feat(api): ajout du service NLP pour la classification"
git push origin feat/nlp-service
```

### 🔁 Faire une Pull Request

* Toujours depuis `feat/...` → vers `dev`
* Puis `dev` → `main` (PR)
* Puis `main` → `prod` (PR)

### 🔐 Branche protégée

Configurer `prod` (et éventuellement `main`) comme branche protégée sur GitHub :

* Interdiction des pushes directs
* Revue obligatoire
* Tests obligatoires si CI

---

## 📌 À faire plus tard

* Mettre en place les tests automatiques (`pytest`)
* Ajouter un hook `pre-push`
* Déploiement automatique depuis `prod`

---

👥 Mainteneur : Thomas
👥 Binôme : Merwan
