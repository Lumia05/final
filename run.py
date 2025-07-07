#!/usr/bin/env python3
"""
Script de démarrage pour l'application ITIL Management System
"""

import os
import sys
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def main():
    print("🚀 Démarrage de l'application ITIL Management System")
    print("=" * 50)
    
    # Vérifier que Flask est installé
    try:
        import flask
        print("✅ Flask est installé")
    except ImportError:
        print("❌ Flask n'est pas installé")
        print("Installez les dépendances avec : pip install -r requirements.txt")
        sys.exit(1)
    
    # Vérifier la configuration
    print("\n📋 Configuration actuelle:")
    print(f"   Host: {os.getenv('MYSQL_HOST', 'localhost')}")
    print(f"   Port: {os.getenv('MYSQL_PORT', '3306')}")
    print(f"   User: {os.getenv('MYSQL_USER', 'root')}")
    print(f"   Database: {os.getenv('MYSQL_DATABASE', 'itil_app')}")
    
    # Importer et démarrer l'application
    try:
        from app import app, init_app
        
        print("\n🔧 Initialisation de l'application...")
        init_app()
        
        print("\n🌐 Démarrage du serveur...")
        print("   URL: http://localhost:5000")
        print("   Admin: admin@admin.com / admin123")
        print("\nAppuyez sur Ctrl+C pour arrêter le serveur")
        
        # Démarrer l'application
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except Exception as e:
        print(f"\n❌ Erreur lors du démarrage: {e}")
        print("\nVérifiez que:")
        print("1. MySQL est démarré")
        print("2. Le fichier .env est configuré")
        print("3. La base de données 'itil_app' existe")
        sys.exit(1)

if __name__ == "__main__":
    main() 