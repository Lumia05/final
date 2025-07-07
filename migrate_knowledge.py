from app import app, db
from sqlalchemy import text

def migrate_knowledge_table():
    print("🔄 Début de la migration de la table knowledge_articles...")
    
    with app.app_context():
        try:
            # Ajout des colonnes manquantes
            db.session.execute(text("""
                ALTER TABLE knowledge_articles
                ADD COLUMN IF NOT EXISTS category VARCHAR(100) NOT NULL DEFAULT 'General',
                ADD COLUMN IF NOT EXISTS status ENUM('DRAFT', 'IN_REVIEW', 'PUBLISHED') NOT NULL DEFAULT 'DRAFT',
                ADD COLUMN IF NOT EXISTS importance ENUM('LOW', 'MEDIUM', 'HIGH', 'CRITICAL') NOT NULL DEFAULT 'MEDIUM',
                ADD COLUMN IF NOT EXISTS validator_id INTEGER,
                ADD FOREIGN KEY (validator_id) REFERENCES users(id);
            """))
            
            # Création de la table tags si elle n'existe pas
            db.session.execute(text("""
                CREATE TABLE IF NOT EXISTS tags (
                    id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(50) NOT NULL UNIQUE
                );
            """))
            
            # Création de la table attachments si elle n'existe pas
            db.session.execute(text("""
                CREATE TABLE IF NOT EXISTS attachments (
                    id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    filename VARCHAR(255) NOT NULL,
                    file_path VARCHAR(512) NOT NULL,
                    article_id INTEGER NOT NULL,
                    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (article_id) REFERENCES knowledge_articles(id)
                );
            """))
            
            # Création des tables de liaison si elles n'existent pas
            db.session.execute(text("""
                CREATE TABLE IF NOT EXISTS article_tags (
                    article_id INTEGER NOT NULL,
                    tag_id INTEGER NOT NULL,
                    PRIMARY KEY (article_id, tag_id),
                    FOREIGN KEY (article_id) REFERENCES knowledge_articles(id),
                    FOREIGN KEY (tag_id) REFERENCES tags(id)
                );
            """))
            
            db.session.execute(text("""
                CREATE TABLE IF NOT EXISTS article_incidents (
                    article_id INTEGER NOT NULL,
                    incident_id INTEGER NOT NULL,
                    PRIMARY KEY (article_id, incident_id),
                    FOREIGN KEY (article_id) REFERENCES knowledge_articles(id),
                    FOREIGN KEY (incident_id) REFERENCES incidents(id)
                );
            """))
            
            db.session.execute(text("""
                CREATE TABLE IF NOT EXISTS article_problems (
                    article_id INTEGER NOT NULL,
                    problem_id INTEGER NOT NULL,
                    PRIMARY KEY (article_id, problem_id),
                    FOREIGN KEY (article_id) REFERENCES knowledge_articles(id),
                    FOREIGN KEY (problem_id) REFERENCES problems(id)
                );
            """))
            
            db.session.commit()
            print("✅ Migration terminée avec succès!")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Erreur lors de la migration : {str(e)}")
            raise

if __name__ == "__main__":
    print("🚀 Démarrage de la migration...")
    migrate_knowledge_table()
    print("🏁 Script terminé.") 