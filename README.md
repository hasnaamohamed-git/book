# Study App - Comprehensive Learning Platform

A modern web application built with React.js frontend and Flask backend, featuring AI-powered translation, summarization, chatbot, PDF viewing, note-taking, and a personal ranking system.

## Features

### 🎯 Core Features

1. **Translation System**
   - Translate text to Arabic and other languages using Google Translate
   - Support for 11+ languages
   - Text-to-speech functionality
   - Copy to clipboard feature

2. **AI Summarization**
   - Generate key points and comprehensive summaries
   - Uses Google's Flan-T5 model
   - Perfect for study materials and research papers

3. **AI Chatbot**
   - Intelligent conversation assistant
   - Powered by Google's Flan-T5-XL model
   - Helpful for answering questions and providing guidance

4. **PDF Viewer**
   - Upload and view PDF documents
   - Page-by-page navigation
   - Text extraction and display
   - Drag-and-drop upload functionality

5. **Note Management**
   - Create and organize notes with sections
   - Drag-and-drop functionality
   - Categories: Lectures, Assignments, Quizzes, Timetable
   - Real-time updates

6. **Personal Ranking System**
   - Points earned for time spent on website
   - Points for asking questions and completing quizzes
   - Leaderboard to track progress
   - Activity tracking

7. **Personal Front Customization**
   - Customize background colors and images
   - Adjust text size, color, and font
   - Personalized dashboard appearance
   - User preferences stored in database

## 🛠️ Technology Stack

### Backend
- **Flask** - Python web framework
- **SQLite** - Database (file-based, no server required)
- **SQLAlchemy** - ORM
- **Flask-Login** - Authentication
- **Flask-CORS** - Cross-origin resource sharing
- **PyPDF2** - PDF processing
- **googletrans** - Translation API
- **transformers** - AI models (Flan-T5)

### Database Management
- **SQLite** - Lightweight, file-based database
- **Automatic setup** - No server installation required
- **Easy backup** - Just copy the `.db` file
- **Admin user** - Created automatically during setup

### Frontend
- **React.js** - UI framework
- **React Router** - Navigation
- **Styled Components** - Styling
- **Framer Motion** - Animations
- **React Dropzone** - File uploads
- **React Beautiful DnD** - Drag and drop
- **Axios** - HTTP client
- **React Hot Toast** - Notifications

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 16+

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd study-app
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database will be automatically created**
   ```bash
   # SQLite database will be created automatically when you first run the app
   # Admin user will be created with credentials: admin/admin123
   # No additional setup required
   ```

5. **Run the backend**
   ```bash
   cd backend
   python app.py
   ```

### Frontend Setup

1. **Install Node.js dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Start the development server**
   ```bash
   npm start
   ```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

## 📁 Project Structure

```
study-app/
├── backend/
│   ├── app.py                 # Main Flask application
│   └── uploads/               # PDF upload directory
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/        # Reusable components
│   │   ├── contexts/          # React contexts
│   │   ├── pages/             # Page components
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
├── requirements.txt
└── README.md
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the backend directory:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///studyapp.db
FLASK_ENV=development
```

### Database Configuration
The SQLite database will be automatically created as `studyapp.db` in the backend directory.

### Database Management
```bash
# Initialize database tables
python manage_db.py init

# Create admin user
python manage_db.py admin

# Show database information
python manage_db.py info

# Reset database (delete all data)
python manage_db.py reset
```

## 🎨 Features in Detail

### Translation System
- **Languages Supported**: English, Arabic, Spanish, French, German, Italian, Portuguese, Russian, Japanese, Korean, Chinese
- **Features**: Text-to-speech, copy to clipboard, language swapping
- **API**: Google Translate integration

### AI Summarization
- **Model**: Google Flan-T5-Base
- **Output**: Key points and comprehensive summary
- **Use Cases**: Study materials, research papers, articles

### PDF Viewer
- **Upload**: Drag-and-drop interface
- **Viewing**: Page-by-page navigation
- **Features**: Text extraction, page counter, file management

### Note Management
- **Sections**: Lectures, Assignments, Quizzes, Timetable
- **Features**: Drag-and-drop reordering, real-time updates
- **Storage**: SQLite database

### Ranking System
- **Points Sources**: Time spent, questions asked, quiz completion
- **Leaderboard**: Top 10 users display
- **Tracking**: Real-time point updates

## 🔒 Security Features

- User authentication with Flask-Login
- Password hashing with Werkzeug
- CORS protection
- File upload validation
- SQL injection prevention with SQLAlchemy

## 📱 Responsive Design

The application is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile phones

## 🚀 Deployment

### Backend Deployment
1. Set up a production server (e.g., Ubuntu with Nginx)
2. Install Python (SQLite is included by default)
3. Configure environment variables
4. Use Gunicorn for production server
5. Set up SSL certificates

### Frontend Deployment
1. Build the production version: `npm run build`
2. Deploy to a static hosting service (Netlify, Vercel, etc.)
3. Configure environment variables for API endpoints

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team

## 🔮 Future Enhancements

- Mobile app development
- Advanced AI features
- Collaborative note-taking
- Video content support
- Advanced analytics dashboard
- Integration with learning management systems# book
