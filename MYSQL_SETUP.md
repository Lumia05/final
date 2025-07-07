# Configuration MySQL pour l'Application ITIL

## Prérequis

1. **MySQL Server** installé et en cours d'exécution
2. **Python** avec les dépendances installées

## Installation des dépendances

```bash
pip install -r requirements.txt
```

## Configuration de la base de données

### 1. Variables d'environnement

Créez un fichier `.env` à la racine du projet avec la configuration suivante :

```env
# Configuration MySQL
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=votre_mot_de_passe
MYSQL_DATABASE=itil_app

# Autres variables d'environnement
ENVIRONMENT=development
```

### 2. Configuration MySQL

Assurez-vous que votre serveur MySQL est configuré pour accepter les connexions avec l'encodage UTF-8 :

```sql
-- Dans MySQL, exécutez :
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;
SET character_set_connection=utf8mb4;
```

### 3. Initialisation de la base de données

Exécutez le script de configuration :

```bash
python setup_mysql.py
```

Ce script va :
- Créer la base de données `itil_app` si elle n'existe pas
- Tester la connexion
- Créer toutes les tables nécessaires

## Démarrage de l'application

Une fois la configuration terminée, démarrez l'application :

```bash
uvicorn app.main:app --reload
```

## Vérification

L'application sera accessible sur `http://localhost:8000`

## Dépannage

### Erreur de connexion
- Vérifiez que MySQL est démarré
- Vérifiez les paramètres de connexion dans le fichier `.env`
- Assurez-vous que l'utilisateur a les droits suffisants

### Erreur d'encodage
- Vérifiez que MySQL utilise l'encodage UTF-8
- Assurez-vous que la base de données est créée avec `utf8mb4`

### Erreur de driver
- Vérifiez que `pymysql` est installé : `pip install pymysql`

## Migration depuis SQLite

Si vous migrez depuis SQLite, vous devrez :

1. Exporter vos données depuis SQLite
2. Les importer dans MySQL
3. Vérifier l'intégrité des données

## Structure de la base de données

L'application crée automatiquement les tables suivantes :
- `incidents` - Gestion des incidents
- `problems` - Gestion des problèmes
- `knowledge_articles` - Base de connaissances 