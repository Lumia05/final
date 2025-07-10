#!/usr/bin/env python3
"""
Application ITIL Management System - Version Flask
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import enum
from sqlalchemy import func

# Configuration Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "supersecretkey123")
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{os.getenv('MYSQL_USER', 'root')}:{os.getenv('MYSQL_PASSWORD', '')}"
    f"@{os.getenv('MYSQL_HOST', 'localhost')}:{os.getenv('MYSQL_PORT', '3306')}"
    f"/{os.getenv('MYSQL_DATABASE', 'itil_app')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuration de l'upload
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialisation des extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
migrate = Migrate(app, db)

# Enums
class Priority(enum.Enum):
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"

class Status(enum.Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"

# Modèles de base de données
class KnowledgeArticle(db.Model):
    __tablename__ = "knowledge_articles"
    
    id = db.Column(db.Integer, primary_key=True, index=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Enum('DRAFT', 'IN_REVIEW', 'PUBLISHED', name='article_status'), default='DRAFT')
    importance = db.Column(db.Enum('LOW', 'MEDIUM', 'HIGH', 'CRITICAL', name='importance_level'), default='MEDIUM')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    validator_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    
    # Relations
    author = db.relationship("User", foreign_keys=[author_id], back_populates="authored_articles")
    validator = db.relationship("User", foreign_keys=[validator_id], back_populates="validated_articles")
    tags = db.relationship("Tag", secondary="article_tags")
    related_incidents = db.relationship("Incident", secondary="article_incidents", back_populates="knowledge_articles")
    related_problems = db.relationship("Problem", secondary="article_problems", back_populates="knowledge_articles")
    attachments = db.relationship("Attachment", back_populates="article")

class Tag(db.Model):
    __tablename__ = "tags"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

class Attachment(db.Model):
    __tablename__ = "attachments"
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(512), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey("knowledge_articles.id"))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    article = db.relationship("KnowledgeArticle", back_populates="attachments")

# Tables de liaison
article_tags = db.Table('article_tags',
    db.Column('article_id', db.Integer, db.ForeignKey('knowledge_articles.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
)

article_incidents = db.Table('article_incidents',
    db.Column('article_id', db.Integer, db.ForeignKey('knowledge_articles.id')),
    db.Column('incident_id', db.Integer, db.ForeignKey('incidents.id'))
)

article_problems = db.Table('article_problems',
    db.Column('article_id', db.Integer, db.ForeignKey('knowledge_articles.id')),
    db.Column('problem_id', db.Integer, db.ForeignKey('problems.id'))
)

class User(UserMixin, db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True, index=True)
    email = db.Column(db.String(255), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    team = db.Column(db.String(255))
    role = db.Column(db.String(20), default="user")  # 'admin' ou 'user'
    
    incidents = db.relationship("Incident", back_populates="assigned_to")
    problems = db.relationship("Problem", back_populates="assigned_to")
    authored_articles = db.relationship("KnowledgeArticle", foreign_keys=[KnowledgeArticle.author_id], back_populates="author")
    validated_articles = db.relationship("KnowledgeArticle", foreign_keys=[KnowledgeArticle.validator_id], back_populates="validator")

class Incident(db.Model):
    __tablename__ = "incidents"
    
    id = db.Column(db.Integer, primary_key=True, index=True)
    title = db.Column(db.String(255), index=True)
    description = db.Column(db.Text)
    priority = db.Column(db.Enum(Priority))
    status = db.Column(db.Enum(Status), default=Status.OPEN)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Champs du post-mortem
    owner = db.Column(db.String(255))
    related_incidents = db.Column(db.Text)
    affected_services = db.Column(db.Text)
    incident_date = db.Column(db.DateTime)
    incident_duration = db.Column(db.String(100))
    response_teams = db.Column(db.Text)
    stakeholders = db.Column(db.Text)
    
    # Détails du post-mortem
    origin = db.Column(db.Text)
    malfunction = db.Column(db.Text)
    impact = db.Column(db.Text)
    detection = db.Column(db.Text)
    response = db.Column(db.Text)
    recovery = db.Column(db.Text)
    
    # 5 Pourquoi
    why1 = db.Column(db.Text)
    why2 = db.Column(db.Text)
    why3 = db.Column(db.Text)
    why4 = db.Column(db.Text)
    why5 = db.Column(db.Text)
    
    # Autres informations
    associated_records = db.Column(db.Text)
    lessons_learned = db.Column(db.Text)
    
    # Relations
    assigned_to_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    assigned_to = db.relationship("User", back_populates="incidents")
    problem_id = db.Column(db.Integer, db.ForeignKey("problems.id"), nullable=True)
    problem = db.relationship("Problem", back_populates="incidents")
    knowledge_articles = db.relationship("KnowledgeArticle", secondary="article_incidents", back_populates="related_incidents")

class Problem(db.Model):
    __tablename__ = "problems"
    
    id = db.Column(db.Integer, primary_key=True, index=True)
    title = db.Column(db.String(255), index=True)
    description = db.Column(db.Text)
    root_cause = db.Column(db.Text)
    status = db.Column(db.Enum(Status), default=Status.OPEN)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    assigned_to_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    assigned_to = db.relationship("User", back_populates="problems")
    incidents = db.relationship("Incident", back_populates="problem")
    knowledge_articles = db.relationship("KnowledgeArticle", secondary="article_problems", back_populates="related_problems")

# Configuration Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Fonction pour créer l'admin par défaut
def create_default_admin():
    admin = User.query.filter_by(role="admin").first()
    if not admin:
        admin_user = User(
            email="admin@admin.com",
            password_hash=generate_password_hash("admin123"),
            is_active=True,
            team="admin",
            role="admin"
        )
        db.session.add(admin_user)
        db.session.commit()
        print("Admin par défaut créé : admin@admin.com / admin123")

# Routes principales
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    # Statistiques
    total_incidents = Incident.query.count()
    total_problems = Problem.query.count()
    total_articles = KnowledgeArticle.query.count()
    
    # Récupérer les 5 incidents les plus récents
    recent_incidents = Incident.query.order_by(Incident.created_at.desc()).limit(5).all()
    
    return render_template('dashboard.html', 
                         total_incidents=total_incidents,
                         total_problems=total_problems,
                         total_articles=total_articles,
                         recent_incidents=recent_incidents)

# Routes d'authentification
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Connexion réussie!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Email ou mot de passe incorrect', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        team = request.form.get('team')
        role = request.form.get('role', 'user')
        
        # Vérifier si l'utilisateur existe déjà
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Cet email est déjà enregistré', 'error')
            return render_template('register.html')
        
        # Créer le nouvel utilisateur
        new_user = User(
            email=email,
            password_hash=generate_password_hash(password),
            team=team,
            role=role
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Inscription réussie! Vous pouvez maintenant vous connecter.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Vous avez été déconnecté', 'info')
    return redirect(url_for('index'))

# Routes pour les incidents
@app.route('/incidents', methods=['GET', 'POST'])
@login_required
def incidents():
    if request.method == 'POST':
        action = request.form.get('action', '')
        if action == 'create':
            # Création d'incident
            title = request.form.get('title', '')
            description = request.form.get('description', '')
            priority = request.form.get('priority', 'P3')
            status = request.form.get('status', 'OPEN')
            assigned_to = request.form.get('assigned_to', '').strip()
            new_incident = Incident(
                title=title,
                description=description,
                priority=Priority[priority],
                status=Status[status],
                owner=assigned_to if assigned_to else 'Non assigné'
            )
            db.session.add(new_incident)
            db.session.commit()
            flash('Incident créé avec succès', 'success')
        elif action.startswith('edit_'):
            incident_id = int(action.split('_')[1])
            incident = Incident.query.get(incident_id)
            if incident:
                incident.title = request.form.get(f'title_{incident_id}', incident.title)
                incident.description = request.form.get(f'description_{incident_id}', incident.description)
                incident.priority = Priority[request.form.get(f'priority_{incident_id}', incident.priority.value)]
                incident.status = Status[request.form.get(f'status_{incident_id}', incident.status.value)]
                incident.owner = request.form.get(f'assigned_to_{incident_id}', incident.owner)
                db.session.commit()
                flash('Incident modifié avec succès', 'success')
        elif action.startswith('delete_'):
            incident_id = int(action.split('_')[1])
            incident = Incident.query.get(incident_id)
            if incident:
                db.session.delete(incident)
                db.session.commit()
                flash('Incident supprimé avec succès', 'success')
        return redirect(url_for('incidents'))

    incidents_list = Incident.query.all()
    return render_template('incidents.html', incidents=incidents_list)

@app.route('/incidents/new', methods=['GET'])
@login_required
def new_incident():
    return render_template('incidents.html', mode='create')

@app.route('/incidents/<int:id>', methods=['GET'])
@login_required
def view_incident(id):
    incident = Incident.query.get_or_404(id)
    return render_template('incidents.html', incident=incident, mode='view')

@app.route('/incidents/delete/<int:incident_id>', methods=['POST'])
@login_required
def delete_incident(incident_id):
    incident = Incident.query.get_or_404(incident_id)
    db.session.delete(incident)
    db.session.commit()
    flash('Incident supprimé avec succès', 'success')
    return redirect(url_for('incidents'))

@app.route('/incidents/edit/<int:incident_id>', methods=['GET', 'POST'])
@login_required
def edit_incident(incident_id):
    incident = Incident.query.get_or_404(incident_id)
    if request.method == 'POST':
        incident.title = request.form.get('title', incident.title)
        incident.description = request.form.get('description', incident.description)
        # Prendre en compte les enums
        priority = request.form.get('priority', incident.priority.value if incident.priority else 'P3')
        status = request.form.get('status', incident.status.value if incident.status else 'OPEN')
        incident.priority = Priority[priority]
        incident.status = Status[status]
        incident.owner = request.form.get('assigned_to', incident.owner)
        db.session.commit()
        flash('Incident modifié avec succès', 'success')
        return redirect(url_for('incidents'))
    return jsonify({
        'id': incident.id,
        'title': incident.title,
        'description': incident.description,
        'priority': incident.priority.value if incident.priority else '',
        'status': incident.status.value if incident.status else '',
        'assigned_to': incident.owner
    })

@app.route('/api/incidents', methods=['POST'])
@login_required
def create_incident():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    # Création de l'incident avec les nouveaux champs
    new_incident = Incident(
        title=data.get('incident_title'),
        description=data.get('summary'),
        priority=data.get('priority'),
        status=Status.OPEN,
        assigned_to_id=current_user.id
    )

    # Ajout des champs supplémentaires dans la base de données
    new_incident.owner = data.get('owner')
    new_incident.related_incidents = data.get('related_incidents')
    new_incident.affected_services = data.get('affected_services')
    new_incident.incident_date = datetime.strptime(data.get('incident_date'), '%Y-%m-%dT%H:%M')
    new_incident.incident_duration = data.get('incident_duration')
    new_incident.response_teams = data.get('response_teams')
    new_incident.stakeholders = data.get('incident_stakeholders')
    
    # Sauvegarde des détails du post-mortem
    new_incident.origin = data.get('origin')
    new_incident.malfunction = data.get('malfunction')
    new_incident.impact = data.get('impact')
    new_incident.detection = data.get('detection')
    new_incident.response = data.get('response')
    new_incident.recovery = data.get('recovery')
    
    # Sauvegarde des 5 pourquoi
    new_incident.why1 = data.get('why1')
    new_incident.why2 = data.get('why2')
    new_incident.why3 = data.get('why3')
    new_incident.why4 = data.get('why4')
    new_incident.why5 = data.get('why5')
    
    # Sauvegarde des autres informations
    new_incident.associated_records = data.get('associated_records')
    new_incident.lessons_learned = data.get('lessons_learned')

    db.session.add(new_incident)
    db.session.commit()

    if request.is_json:
        return jsonify({"message": "Incident créé avec succès", "id": new_incident.id}), 201
    else:
        flash('Incident créé avec succès', 'success')
        return redirect(url_for('incidents'))

# Routes pour les problèmes
@app.route('/problems', methods=['GET', 'POST'])
@login_required
def problems():
    if request.method == 'POST':
        context = request.form.get('problem_context', '')
        desc = request.form.get('incident_desc', '')
        status = request.form.get('status', 'OPEN')
        why1 = request.form.get('why1', '')
        why2 = request.form.get('why2', '')
        why3 = request.form.get('why3', '')
        why4 = request.form.get('why4', '')
        why5 = request.form.get('why5', '')
        root_cause = request.form.get('root_cause', '')
        solutions = request.form.get('suggested_solutions', '')

        # On concatène les 5 pourquoi et les solutions dans la description pour ne rien perdre
        full_description = f"{desc}\n\nAnalyse des 5 Pourquoi:\n1. {why1}\n2. {why2}\n3. {why3}\n4. {why4}\n5. {why5}\n\nSolutions suggérées:\n{solutions}"

        new_problem = Problem(
            title=context,
            description=full_description,
            root_cause=root_cause,
            status=status
        )
        db.session.add(new_problem)
        db.session.commit()
        flash('Problème enregistré avec succès !', 'success')
        return redirect(url_for('problems'))
    return render_template('problems.html')

@app.route('/api/problems', methods=['POST'])
@login_required
def create_problem():
    data = request.get_json()
    
    new_problem = Problem(
        title=data['title'],
        description=data['description'],
        root_cause=data.get('root_cause', ''),
        assigned_to_id=data.get('assigned_to_id')
    )
    
    db.session.add(new_problem)
    db.session.commit()
    
    return jsonify({'message': 'Problème créé avec succès', 'id': new_problem.id}), 201

@app.route('/users')
@login_required
def users():
    q = request.args.get('q', '').strip()
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    query = User.query
    if q:
        query = query.filter((User.email.contains(q)) | (User.team.contains(q)) | (User.role.contains(q)))
    pagination = query.order_by(User.id.desc()).paginate(page=page, per_page=per_page, error_out=False)
    users = pagination.items
    return render_template('users.html', users=users, pagination=pagination, q=q, per_page=per_page)

# Routes pour la base de connaissances
@app.route('/knowledge')
@login_required
def knowledge():
    articles = KnowledgeArticle.query.order_by(KnowledgeArticle.created_at.desc()).all()
    return render_template('knowledge.html', articles=articles)

@app.route('/knowledge/<int:id>')
@login_required
def view_knowledge_article(id):
    article = KnowledgeArticle.query.get_or_404(id)
    return render_template('view_knowledge_article.html', article=article)

@app.route('/knowledge/create', methods=['GET', 'POST'])
@login_required
def create_knowledge_article():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category = request.form['category']
        importance = request.form['importance']
        tags_str = request.form['tags']
        
        new_article = KnowledgeArticle(
            title=title,
            content=content,
            category=category,
            importance=importance,
            author_id=current_user.id
        )
        
        # Gestion des tags
        if tags_str:
            tag_names = [name.strip() for name in tags_str.split(',')]
            for tag_name in tag_names:
                tag = Tag.query.filter_by(name=tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name)
                    db.session.add(tag)
                new_article.tags.append(tag)
        
        db.session.add(new_article)
        db.session.commit()

        # Gestion des pièces jointes
        files = request.files.getlist('attachments')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                attachment = Attachment(
                    filename=filename,
                    file_path=filepath,
                    article_id=new_article.id
                )
                db.session.add(attachment)
        
        db.session.commit()
        
        flash('Article créé avec succès!', 'success')
        return redirect(url_for('knowledge'))
        
    return render_template('create_knowledge_article.html')

@app.route('/knowledge/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_knowledge_article(id):
    article = KnowledgeArticle.query.get_or_404(id)
    
    # Vérifier si l'utilisateur est l'auteur ou un admin
    if not (current_user.id == article.author_id or current_user.role == 'admin'):
        flash('Vous n\'avez pas la permission de modifier cet article.', 'error')
        return redirect(url_for('knowledge'))
    
    if request.method == 'POST':
        article.title = request.form['title']
        article.content = request.form['content']
        article.category = request.form['category']
        article.importance = request.form['importance']
        
        # Mise à jour des tags
        article.tags.clear()
        tags_str = request.form['tags']
        if tags_str:
            tag_names = [name.strip() for name in tags_str.split(',')]
            for tag_name in tag_names:
                tag = Tag.query.filter_by(name=tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name)
                    db.session.add(tag)
                article.tags.append(tag)
        
        # Gestion des nouvelles pièces jointes
        files = request.files.getlist('attachments')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                attachment = Attachment(
                    filename=filename,
                    file_path=filepath,
                    article_id=article.id
                )
                db.session.add(attachment)
        
        db.session.commit()
        flash('Article mis à jour avec succès!', 'success')
        return redirect(url_for('view_knowledge_article', id=article.id))
    
    return render_template('edit_knowledge_article.html', article=article)

@app.route('/knowledge/<int:id>/delete', methods=['POST'])
@login_required
def delete_knowledge_article(id):
    article = KnowledgeArticle.query.get_or_404(id)
    
    # Vérifier si l'utilisateur est l'auteur ou un admin
    if not (current_user.id == article.author_id or current_user.role == 'admin'):
        return jsonify({'success': False, 'message': 'Permission denied'}), 403
    
    try:
        # Supprimer les pièces jointes
        for attachment in article.attachments:
            try:
                os.remove(attachment.file_path)
            except OSError:
                pass  # Ignorer les erreurs si le fichier n'existe pas
        
        db.session.delete(article)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/knowledge/attachment/<int:id>/delete', methods=['POST'])
@login_required
def delete_attachment(id):
    attachment = Attachment.query.get_or_404(id)
    article = attachment.article
    
    # Vérifier si l'utilisateur est l'auteur de l'article ou un admin
    if not (current_user.id == article.author_id or current_user.role == 'admin'):
        return jsonify({'success': False, 'message': 'Permission denied'}), 403
    
    try:
        # Supprimer le fichier physique
        try:
            os.remove(attachment.file_path)
        except OSError:
            pass  # Ignorer les erreurs si le fichier n'existe pas
        
        # Supprimer l'enregistrement de la base de données
        db.session.delete(attachment)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/knowledge', methods=['POST'])
@login_required
def search_knowledge():
    query = request.args.get('q', '')
    if query:
        articles = KnowledgeArticle.query.filter(
            db.or_(
                KnowledgeArticle.title.contains(query),
                KnowledgeArticle.content.contains(query),
                KnowledgeArticle.tags.contains(query)
            )
        ).all()
    else:
        articles = KnowledgeArticle.query.all()
    
    return jsonify([{
        'id': article.id,
        'title': article.title,
        'content': article.content[:200] + '...' if len(article.content) > 200 else article.content,
        'tags': article.tags,
        'created_at': article.created_at.strftime('%Y-%m-%d %H:%M')
    } for article in articles])

@app.route('/api/knowledge/suggest')
@login_required
def suggest_knowledge_articles():
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify([])
    # Recherche simple : LIKE sur le titre et le contenu
    articles = KnowledgeArticle.query.filter(
        db.or_(
            KnowledgeArticle.title.ilike(f'%{query}%'),
            KnowledgeArticle.content.ilike(f'%{query}%')
        )
    ).order_by(KnowledgeArticle.created_at.desc()).limit(5).all()
    return jsonify([
        {
            'id': a.id,
            'title': a.title,
            'content': a.content[:120] + ('...' if len(a.content) > 120 else '')
        } for a in articles
    ])

# API pour obtenir les données
@app.route('/api/incidents')
@login_required
def get_incidents():
    incidents = Incident.query.all()
    return jsonify([{
        'id': incident.id,
        'title': incident.title,
        'description': incident.description,
        'priority': incident.priority.value if incident.priority else None,
        'status': incident.status.value if incident.status else None,
        'created_at': incident.created_at.strftime('%Y-%m-%d %H:%M'),
        'assigned_to': incident.assigned_to.email if incident.assigned_to else None
    } for incident in incidents])

@app.route('/api/problems')
@login_required
def get_problems():
    problems = Problem.query.all()
    return jsonify([{
        'id': problem.id,
        'title': problem.title,
        'description': problem.description,
        'root_cause': problem.root_cause,
        'status': problem.status.value if problem.status else None,
        'created_at': problem.created_at.strftime('%Y-%m-%d %H:%M'),
        'assigned_to': problem.assigned_to.email if problem.assigned_to else None
    } for problem in problems])

@app.route('/api/users')
@login_required
def get_users():
    users = User.query.filter_by(is_active=True).all()
    return jsonify([{
        'id': user.id,
        'email': user.email,
        'team': user.team,
        'role': user.role
    } for user in users])

@app.route('/api/problems/suggest_root_cause', methods=['POST'])
@login_required
def suggest_root_cause():
    data = request.get_json()
    why1 = data.get('why1', '')
    why2 = data.get('why2', '')
    why3 = data.get('why3', '')
    why4 = data.get('why4', '')
    why5 = data.get('why5', '')

    # Logique simple : la cause racine est le dernier pourquoi non vide
    root_cause = why5 or why4 or why3 or why2 or why1 or "Non déterminée"

    # Générer des solutions génériques
    solutions = [
        f"Mettre en place des mesures pour éviter la récurrence de : {root_cause}",
        "Former les équipes sur la détection précoce de ce type de problème",
        "Établir des procédures de contrôle et de suivi",
        "Mettre en place des indicateurs pour mesurer l'efficacité des solutions"
    ]
    return jsonify({
        'root_cause': root_cause,
        'solutions': solutions
    })

@app.route('/api/dashboard_stats')
@login_required
def dashboard_stats():
    # Incidents par statut
    incident_status_raw = db.session.query(Incident.status, func.count()).group_by(Incident.status).all()
    incident_status_counts = {status.name: count for status, count in incident_status_raw}
    
    # Problèmes par statut
    problem_status_raw = db.session.query(Problem.status, func.count()).group_by(Problem.status).all()
    problem_status_counts = {status.name: count for status, count in problem_status_raw}

    # Evolution incidents par mois (6 derniers mois)
    incident_evolution_raw = db.session.query(
        func.date_format(Incident.created_at, '%Y-%m'), func.count()
    ).group_by(func.date_format(Incident.created_at, '%Y-%m')).order_by(func.date_format(Incident.created_at, '%Y-%m').desc()).limit(6).all()
    
    # Evolution problèmes par mois (6 derniers mois)
    problem_evolution_raw = db.session.query(
        func.date_format(Problem.created_at, '%Y-%m'), func.count()
    ).group_by(func.date_format(Problem.created_at, '%Y-%m')).order_by(func.date_format(Problem.created_at, '%Y-%m').desc()).limit(6).all()
    
    # Transformer les Row en dictionnaires/listes qui sont JSON serializables
    incident_evolution = [{'date': date, 'count': count} for date, count in reversed(incident_evolution_raw)]
    problem_evolution = [{'date': date, 'count': count} for date, count in reversed(problem_evolution_raw)]

    return jsonify({
        'incident_status': incident_status_counts,
        'problem_status': problem_status_counts,
        'incident_evolution': incident_evolution,
        'problem_evolution': problem_evolution
    })

@app.route('/suggest_knowledge', methods=['POST'])
@login_required
def suggest_knowledge():
    query = request.json.get('query', '').lower()
    if not query:
        return jsonify([])
    # Recherche simple par similarité dans le titre ou le contenu
    articles = KnowledgeArticle.query.all()
    suggestions = []
    for article in articles:
        if query in (article.title or '').lower() or query in (article.content or '').lower():
            suggestions.append({
                'id': article.id,
                'title': article.title,
                'url': url_for('view_knowledge_article', id=article.id)
            })
        elif any(word in (article.title or '').lower() or word in (article.content or '').lower() for word in query.split()):
            suggestions.append({
                'id': article.id,
                'title': article.title,
                'url': url_for('view_knowledge_article', id=article.id)
            })
        if len(suggestions) >= 5:
            break
    return jsonify(suggestions)

# Gestion des erreurs
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

# Initialisation de l'application
def init_app():
    with app.app_context():
        # Créer toutes les tables
        db.create_all()
        # Créer l'admin par défaut
        create_default_admin()
        print("✅ Application Flask initialisée avec succès!")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    init_app()
    app.run(debug=True, host='0.0.0.0', port=5000) 