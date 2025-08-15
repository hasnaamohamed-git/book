#!/bin/bash

echo "🚀 Setting up Study App..."
echo "================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ first."
    exit 1
fi

echo "✅ SQLite will be used as the database (no additional setup required)"

echo "✅ Prerequisites check completed"

# Create virtual environment
echo "📦 Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
cd frontend
npm install
cd ..

# Create uploads directory
echo "📁 Creating uploads directory..."
mkdir -p backend/uploads

# Create .env file
echo "⚙️  Creating environment file..."
cat > backend/.env << EOF
SECRET_KEY=your-secret-key-here-change-this-in-production
DATABASE_URL=sqlite:///studyapp.db
FLASK_ENV=development
EOF

# Initialize database
echo "🗄️  Initializing database..."
cd backend
python manage_db.py init
python manage_db.py admin
cd ..

echo "✅ Setup completed!"
echo ""
echo "🔑 Default admin credentials:"
echo "   Username: admin"
echo "   Password: admin123"
echo ""
echo "📋 Next steps:"
echo "1. Start the backend: cd backend && python app.py"
echo "2. Start the frontend: cd frontend && npm start"
echo ""
echo "🌐 The application will be available at:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:5000"
echo ""
echo "📚 For more information, see the README.md file"