import os

def setup_uploads():
    # Chemin du dossier d'uploads
    upload_dir = os.path.join('static', 'uploads')
    
    # Créer le dossier s'il n'existe pas
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
        print(f"✅ Dossier '{upload_dir}' créé avec succès!")
    else:
        print(f"ℹ️ Le dossier '{upload_dir}' existe déjà.")
    
    # Vérifier les permissions
    try:
        test_file = os.path.join(upload_dir, 'test.txt')
        with open(test_file, 'w') as f:
            f.write('Test write permissions')
        os.remove(test_file)
        print("✅ Permissions d'écriture OK!")
    except Exception as e:
        print(f"❌ Erreur de permissions : {str(e)}")
        print("⚠️ Assurez-vous que l'application a les droits d'écriture dans le dossier.")

if __name__ == "__main__":
    print("🚀 Configuration du dossier d'uploads...")
    setup_uploads()
    print("🏁 Configuration terminée.") 