# ITIL Management System - Flask

Système de gestion ITIL moderne basé sur Flask pour la gestion des incidents, problèmes et base de connaissances.

## 🚀 Fonctionnalités

- **Gestion des Incidents** : Création, suivi et résolution des incidents
- **Gestion des Problèmes** : Identification et résolution des causes racines
- **Base de Connaissances** : Articles et solutions centralisées
- **Authentification** : Système de connexion sécurisé avec gestion des rôles
- **Dashboard** : Tableaux de bord avec statistiques
- **Interface Moderne** : Design responsive et professionnel

## 🛠️ Technologies

- **Backend** : Flask 2.3.3
- **Base de données** : MySQL avec SQLAlchemy
- **Authentification** : Flask-Login
- **Frontend** : HTML5, CSS3, JavaScript
- **Icônes** : Font Awesome
- **Design** : Interface moderne et responsive

## 📋 Prérequis

- Python 3.8+
- MySQL Server
- pip (gestionnaire de paquets Python)

## 🔧 Installation

### 1. Cloner le projet
```bash
git clone <votre-repo>
cd final
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3. Configuration de la base de données

#### Option A : Utiliser XAMPP (recommandé)
1. Téléchargez et installez [XAMPP](https://www.apachefriends.org/)
2. Démarrez Apache et MySQL dans XAMPP
3. Créez une base de données nommée `itil_app`

#### Option B : MySQL standalone
1. Installez MySQL Server
2. Créez une base de données : `CREATE DATABASE itil_app;`

### 4. Configuration des variables d'environnement

Créez un fichier `.env` à la racine du projet :
```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=votre_mot_de_passe
MYSQL_DATABASE=itil_app
SECRET_KEY=votre_clé_secrète_ici
```

### 5. Initialiser la base de données
```bash
python setup_mysql.py
```

## 🚀 Démarrage

### Démarrage simple
```bash
python app.py
```

L'application sera accessible sur : `http://localhost:5000`

### Démarrage en mode développement
```bash
python app.py
```
- Mode debug activé
- Rechargement automatique des fichiers
- Messages d'erreur détaillés

## 👤 Comptes par défaut

### Administrateur
- **Email** : `admin@admin.com`
- **Mot de passe** : `admin123`
- **Rôle** : Administrateur (accès complet)

### Créer un nouvel utilisateur
1. Allez sur `/register`
2. Remplissez le formulaire
3. Choisissez le rôle (user/admin)

## 📁 Structure du projet

```
final/
├── app.py                 # Application Flask principale
├── setup_mysql.py         # Script d'initialisation MySQL
├── requirements.txt       # Dépendances Python
├── .env                   # Variables d'environnement
├── templates/             # Templates HTML
│   ├── base.html         # Template de base
│   ├── index.html        # Page d'accueil
│   ├── login.html        # Page de connexion
│   ├── register.html     # Page d'inscription
│   ├── dashboard.html    # Tableau de bord
│   ├── incidents.html    # Gestion des incidents
│   ├── problems.html     # Gestion des problèmes
│   └── knowledge.html    # Base de connaissances
├── static/               # Fichiers statiques
│   ├── style.css        # Styles CSS
│   └── script.js        # JavaScript
└── data/                # Données JSON (si applicable)
```

## 🔐 Sécurité

- **Authentification** : Flask-Login avec sessions sécurisées
- **Mots de passe** : Hashage avec Werkzeug
- **Rôles** : Gestion des permissions (admin/user)
- **CSRF** : Protection contre les attaques CSRF
- **Validation** : Validation des données côté serveur

## 📊 Fonctionnalités détaillées

### Gestion des Incidents
- Création d'incidents avec priorité (P1, P2, P3)
- Statuts : Ouvert, En cours, Résolu, Fermé
- Assignment aux membres de l'équipe
- Historique des modifications

### Gestion des Problèmes
- Identification des causes racines
- Liaison avec les incidents
- Suivi de la résolution
- Documentation des solutions

### Base de Connaissances
- Articles avec titre, contenu et tags
- Recherche textuelle
- Catégorisation par tags
- Historique des modifications

### Dashboard
- Statistiques en temps réel
- Graphiques des incidents/problèmes
- Vue d'ensemble de l'activité
- Métriques de performance

## 🛠️ Développement

### Ajouter une nouvelle fonctionnalité
1. Créer la route dans `app.py`
2. Ajouter le template HTML dans `templates/`
3. Mettre à jour les styles dans `static/style.css`
4. Tester la fonctionnalité

### Modifier la base de données
1. Modifier les modèles dans `app.py`
2. Exécuter `python setup_mysql.py` pour recréer les tables
3. Ou utiliser des migrations SQLAlchemy

## 📝 API Endpoints

### Authentification
- `POST /login` - Connexion
- `POST /register` - Inscription
- `GET /logout` - Déconnexion

### Incidents
- `GET /incidents` - Liste des incidents
- `POST /api/incidents` - Créer un incident
- `GET /api/incidents` - API incidents

### Problèmes
- `GET /problems` - Liste des problèmes
- `POST /api/problems` - Créer un problème
- `GET /api/problems` - API problèmes

### Base de Connaissances
- `GET /knowledge` - Liste des articles
- `POST /api/knowledge` - Créer un article
- `GET /api/knowledge/search` - Recherche d'articles

## 🐛 Dépannage

### Erreur de connexion MySQL
- Vérifiez que MySQL est démarré
- Vérifiez les paramètres dans `.env`
- Testez la connexion : `python setup_mysql.py`

### Erreur "No module named 'flask'"
```bash
pip install -r requirements.txt
```

### Erreur de port déjà utilisé
- Changez le port dans `app.py` : `app.run(port=5001)`
- Ou arrêtez le processus utilisant le port 5000

## 📞 Support

Pour toute question ou problème :
1. Vérifiez la section dépannage
2. Consultez les logs de l'application
3. Vérifiez la configuration MySQL

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

---

**ITIL Management System** - Gestion moderne des services IT avec Flask 