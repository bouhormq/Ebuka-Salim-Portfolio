#!/bin/bash

# Flask Portfolio Server Startup Script

echo "🚀 Starting Flask Portfolio Server..."
echo "🔧 Setting up environment..."

# Navigate to project directory
cd /Users/salim/Desktop/Ebuka-Salim-Portfolio

# Start server without debug mode to avoid reloader issues
echo "📡 Starting server on port 5001..."
/Users/salim/Desktop/Ebuka-Salim-Portfolio/.venv/bin/python -c "
from app import app
print('🌐 Server starting at http://localhost:5001')
print('📡 API endpoints available:')
print('   GET  /api/timeline_post')
print('   POST /api/timeline_post')
print('   DELETE /api/timeline_post/<id>')
print('💡 Use Ctrl+C to stop the server')
print('-' * 50)
app.run(host='0.0.0.0', port=5001)
"
