#!/usr/bin/env python3
"""
Script de configuration et initialisation de la base de données MySQL
"""

import os
import pymysql
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

def setup_database():
    load_dotenv()

    # --- Configuration ---
    db_user = os.getenv('MYSQL_USER', 'root')
    db_password = os.getenv('MYSQL_PASSWORD', '')
    db_host = os.getenv('MYSQL_HOST', 'localhost')
    db_port = int(os.getenv('MYSQL_PORT', 3306))
    db_name = os.getenv('MYSQL_DATABASE', 'itil_app')

    # --- Connexion sans base de données spécifique ---
    try:
        engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}")
        with engine.connect() as connection:
            print("✅ Connexion à MySQL réussie.")
            # Supprimer la base de données si elle existe
            connection.execute(text(f"DROP DATABASE IF EXISTS {db_name}"))
            print(f"🗑️ Base de données '{db_name}' supprimée si elle existait.")
            # Créer la base de données
            connection.execute(text(f"CREATE DATABASE {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
            print(f"✅ Base de données '{db_name}' créée.")
    except Exception as e:
        print(f"❌ Erreur de connexion ou de création de la base de données : {e}")
        return

    # --- Initialisation de l'application Flask et des tables ---
    # On importe ici pour éviter les problèmes d'imports circulaires/contextuels
    from app import app, db, User

    with app.app_context():
        # Créer toutes les tables
        db.create_all()
        print("✅ Tables créées avec succès.")
        
        # Création de l'admin par défaut
        if not User.query.filter_by(email="admin@admin.com").first():
            from werkzeug.security import generate_password_hash
            admin = User(
                email="admin@admin.com",
                hashed_password=generate_password_hash("admin123"),
                role="admin",
                is_active=True
            )
            db.session.add(admin)
            db.session.commit()
            print("✅ Administrateur par défaut créé.")

if __name__ == "__main__":
    print("🚀 Démarrage du script de configuration de la base de données...")
    setup_database()
    print("🏁 Script terminé.") 