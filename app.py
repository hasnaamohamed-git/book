from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime, timedelta
import PyPDF2
import io
from googletrans import Translator
from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///studyapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

CORS(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

# Initialize AI models
translator = Translator()
tokenizer_summary = T5Tokenizer.from_pretrained('google/flan-t5-base')
model_summary = T5ForConditionalGeneration.from_pretrained('google/flan-t5-base')
tokenizer_chatbot = T5Tokenizer.from_pretrained('google/flan-t5-xl')
model_chatbot = T5ForConditionalGeneration.from_pretrained('google/flan-t5-xl')

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    points = db.Column(db.Integer, default=0)
    time_spent = db.Column(db.Integer, default=0)  # in minutes
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    preferences = db.Column(db.Text, default='{}')  # Store as JSON string for SQLite
    
    notes = db.relationship('Note', backref='user', lazy=True)
    activities = db.relationship('UserActivity', backref='user', lazy=True)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text)
    section = db.Column(db.String(50), nullable=False)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class UserActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activity_type = db.Column(db.String(50), nullable=False)  # 'time_spent', 'question_asked', 'quiz_correct'
    points_earned = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class PDFDocument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    pages = db.Column(db.Text)  # Store page content as JSON string for SQLite
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Translation function
def translate_text(text, dest='ar'):
    try:
        translation = translator.translate(text, dest=dest)
        return translation.text
    except Exception as e:
        return f"Translation error: {str(e)}"

# Summarization function
def summarize_text(text):
    try:
        # Generate key points
        key_points_prompt = f"Generate key points from this text: {text[:1000]}"
        inputs = tokenizer_summary(key_points_prompt, return_tensors="pt", max_length=512, truncation=True)
        key_points_output = model_summary.generate(**inputs, max_length=150, num_beams=4)
        key_points = tokenizer_summary.decode(key_points_output[0], skip_special_tokens=True)
        
        # Generate overall summary
        summary_prompt = f"Summarize this text: {text[:1000]}"
        inputs = tokenizer_summary(summary_prompt, return_tensors="pt", max_length=512, truncation=True)
        summary_output = model_summary.generate(**inputs, max_length=200, num_beams=4)
        summary = tokenizer_summary.decode(summary_output[0], skip_special_tokens=True)
        
        return {
            'key_points': key_points,
            'summary': summary
        }
    except Exception as e:
        return {
            'key_points': f"Error generating key points: {str(e)}",
            'summary': f"Error generating summary: {str(e)}"
        }

# Chatbot function
def chatbot_response(text):
    try:
        prompt = f"User: {text}\nAssistant:"
        inputs = tokenizer_chatbot(prompt, return_tensors="pt", max_length=512, truncation=True)
        outputs = model_chatbot.generate(**inputs, max_length=200, num_beams=4)
        response = tokenizer_chatbot.decode(outputs[0], skip_special_tokens=True)
        return response
    except Exception as e:
        return f"I'm sorry, I encountered an error: {str(e)}"

# Routes
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    user = User(
        username=data['username'],
        email=data['email'],
        password_hash=generate_password_hash(data['password'])
    )
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    
    if user and check_password_hash(user.password_hash, data['password']):
        login_user(user)
        return jsonify({'message': 'Logged in successfully', 'user_id': user.id})
    
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/user')
@login_required
def get_user():
    return jsonify({
        'id': current_user.id,
        'username': current_user.username,
        'email': current_user.email,
        'points': current_user.points,
        'time_spent': current_user.time_spent
    })

@app.route('/api/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'})

@app.route('/api/translate', methods=['POST'])
@login_required
def translate():
    data = request.get_json()
    translated_text = translate_text(data['text'], data.get('dest', 'ar'))
    return jsonify({'translated_text': translated_text})

@app.route('/api/summarize', methods=['POST'])
@login_required
def summarize():
    data = request.get_json()
    result = summarize_text(data['text'])
    return jsonify(result)

@app.route('/api/chatbot', methods=['POST'])
@login_required
def chatbot():
    data = request.get_json()
    response = chatbot_response(data['message'])
    return jsonify({'response': response})

@app.route('/api/notes', methods=['GET'])
@login_required
def get_notes():
    notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.section, Note.order).all()
    return jsonify([{
        'id': note.id,
        'title': note.title,
        'content': note.content,
        'section': note.section,
        'order': note.order,
        'created_at': note.created_at.isoformat(),
        'updated_at': note.updated_at.isoformat()
    } for note in notes])

@app.route('/api/notes', methods=['POST'])
@login_required
def create_note():
    data = request.get_json()
    note = Note(
        title=data['title'],
        content=data.get('content', ''),
        section=data['section'],
        user_id=current_user.id
    )
    db.session.add(note)
    db.session.commit()
    return jsonify({'id': note.id, 'message': 'Note created successfully'})

@app.route('/api/notes/<int:note_id>', methods=['PUT'])
@login_required
def update_note(note_id):
    note = Note.query.filter_by(id=note_id, user_id=current_user.id).first()
    if not note:
        return jsonify({'error': 'Note not found'}), 404
    
    data = request.get_json()
    note.title = data.get('title', note.title)
    note.content = data.get('content', note.content)
    note.section = data.get('section', note.section)
    note.order = data.get('order', note.order)
    note.updated_at = datetime.utcnow()
    
    db.session.commit()
    return jsonify({'message': 'Note updated successfully'})

@app.route('/api/notes/<int:note_id>', methods=['DELETE'])
@login_required
def delete_note(note_id):
    note = Note.query.filter_by(id=note_id, user_id=current_user.id).first()
    if not note:
        return jsonify({'error': 'Note not found'}), 404
    
    db.session.delete(note)
    db.session.commit()
    return jsonify({'message': 'Note deleted successfully'})

@app.route('/api/upload-pdf', methods=['POST'])
@login_required
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'Only PDF files are allowed'}), 400
    
    try:
        # Read PDF content
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
        pages = []
        
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            pages.append({
                'page_number': page_num + 1,
                'content': text
            })
        
        # Save to database
        filename = secure_filename(file.filename)
        pdf_doc = PDFDocument(
            filename=filename,
            original_filename=file.filename,
            pages=json.dumps(pages),
            user_id=current_user.id
        )
        
        db.session.add(pdf_doc)
        db.session.commit()
        
        return jsonify({
            'id': pdf_doc.id,
            'filename': filename,
            'pages': pages,
            'message': 'PDF uploaded successfully'
        })
        
    except Exception as e:
        return jsonify({'error': f'Error processing PDF: {str(e)}'}), 500

@app.route('/api/pdfs', methods=['GET'])
@login_required
def get_pdfs():
    pdfs = PDFDocument.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': pdf.id,
        'filename': pdf.filename,
        'original_filename': pdf.original_filename,
        'pages': json.loads(pdf.pages) if pdf.pages else [],
        'created_at': pdf.created_at.isoformat()
    } for pdf in pdfs])

@app.route('/api/points/add', methods=['POST'])
@login_required
def add_points():
    data = request.get_json()
    points = data.get('points', 0)
    activity_type = data.get('activity_type', 'other')
    
    current_user.points += points
    
    activity = UserActivity(
        activity_type=activity_type,
        points_earned=points,
        user_id=current_user.id
    )
    
    db.session.add(activity)
    db.session.commit()
    
    return jsonify({'points': current_user.points, 'message': 'Points added successfully'})

@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    users = User.query.order_by(User.points.desc()).limit(10).all()
    return jsonify([{
        'username': user.username,
        'points': user.points,
        'time_spent': user.time_spent
    } for user in users])

@app.route('/api/preferences', methods=['GET'])
@login_required
def get_preferences():
    try:
        preferences = json.loads(current_user.preferences) if current_user.preferences else {}
        return jsonify(preferences)
    except json.JSONDecodeError:
        return jsonify({})

@app.route('/api/preferences', methods=['PUT'])
@login_required
def update_preferences():
    data = request.get_json()
    current_user.preferences = json.dumps(data)
    db.session.commit()
    return jsonify({'message': 'Preferences updated successfully'})

@app.route('/api/time-spent', methods=['POST'])
@login_required
def update_time_spent():
    data = request.get_json()
    minutes = data.get('minutes', 0)
    
    current_user.time_spent += minutes
    points_earned = minutes // 5  # 1 point per 5 minutes
    
    if points_earned > 0:
        current_user.points += points_earned
        activity = UserActivity(
            activity_type='time_spent',
            points_earned=points_earned,
            user_id=current_user.id
        )
        db.session.add(activity)
    
    db.session.commit()
    
    return jsonify({
        'time_spent': current_user.time_spent,
        'points': current_user.points,
        'points_earned': points_earned
    })

def init_db():
    """Initialize the database and create tables"""
    with app.app_context():
        db.create_all()
        print("✅ Database initialized successfully!")

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)