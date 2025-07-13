# Production Engineering - Portfolio Site with Timeline API

Welcome to the MLH Fellowship Portfolio! This Flask-based portfolio site now includes a full-featured timeline post API with MySQL database integration. The site showcases personal information while providing a robust backend for timeline posts with CRUD operations.

## 🚀 Features

### Portfolio Pages
- ✅ **Home Page** - Landing page with profile information
- ✅ **About** - Personal description with edit functionality
- ✅ **Work Experience** - Professional background with add/edit features
- ✅ **Education** - Academic history with form input
- ✅ **Hobbies** - Personal interests with image uploads
- ✅ **Travel** - Interactive map of visited locations

### Timeline Post API
- ✅ **REST API** for timeline posts (Create, Read, Delete)
- ✅ **MySQL Database** integration with Peewee ORM
- ✅ **Data Persistence** across server restarts
- ✅ **Error Handling** and validation
- ✅ **Automated Testing** with curl scripts

## Tasks

Once you've got your portfolio downloaded and running using the instructions below, you should attempt to complete the following tasks.

For each of these tasks, you should create an [Issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/about-issues) and work on them in a new [branch](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-branches). When the task has been completed, you should open a [Pull Request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests) and get another fellow in your pod to give you feedback before merging it in.

*Note: Make sure to include a link to the Issue you're progressing on inside of your Pull Request so your reviewer knows what you're progressing on!*

### GitHub Tasks
- [x] Create Issues for each task below
- [x] Progress on each task in a new branch
- [x] Open a Pull Request when a task is finished to get feedback

### Portfolio Tasks
- [x] Add a photo of yourself to the website
- [x] Add an "About youself" section to the website.
- [x] Add your previous work experiences
- [x] Add your hobbies (including images)
- [x] Add your current/previous education
- [x] Add a map of all the cool locations/countries you visited

### Flask Tasks
- [x] Get your Flask app running locally on your machine using the instructions below.
- [x] Add a template for adding multiple work experiences/education/hobbies using [Jinja](https://jinja.palletsprojects.com/en/3.0.x/api/#basics)
- [x] Create a new page to display hobbies.
- [x] Add a menu bar that dynamically displays other pages in the app

### Database & API Tasks
- [x] **MySQL Database Integration** - Connect Flask app to MySQL database using Peewee ORM
- [x] **Timeline Post Model** - Create database model for timeline posts with fields: name, email, content, created_at
- [x] **REST API Endpoints** - Implement GET, POST, and DELETE endpoints for timeline posts
- [x] **API Testing** - Create automated curl testing script for all endpoints
- [x] **Error Handling** - Add comprehensive error handling and logging


## 🛠 Installation & Setup

### Prerequisites
- Python 3.11+ installed
- MySQL server running locally
- pip package manager

### Environment Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd Ebuka-Salim-Portfolio
```

2. **Create and activate virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Database Configuration**
```bash
# Copy environment template
cp example.env .env

# Edit .env file with your MySQL credentials:
# MYSQL_HOST=localhost
# MYSQL_USER=your_username
# MYSQL_PASSWORD=your_password
# MYSQL_DATABASE=your_database_name
# URL=localhost:5001
```

5. **Database Setup**
   - Create a MySQL database with the name specified in your `.env` file
   - The application will automatically create the required tables on first run

### Running the Application

**Option 1: Using the startup script (Recommended)**
```bash
./start_server.sh
```

**Option 2: Manual start**
```bash
python -c "from app import app; app.run(host='0.0.0.0', port=5001)"
```

The application will be available at: **http://localhost:5001**

### API Endpoints

The application provides the following REST API endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/timeline_post` | Retrieve all timeline posts |
| `POST` | `/api/timeline_post` | Create a new timeline post |
| `DELETE` | `/api/timeline_post/<id>` | Delete a specific timeline post |

#### API Usage Examples

**Create a timeline post:**
```bash
curl -X POST http://localhost:5001/api/timeline_post \
  -d "name=John Doe" \
  -d "email=john@example.com" \
  -d "content=Hello World!"
```

**Get all timeline posts:**
```bash
curl http://localhost:5001/api/timeline_post
```

**Delete a timeline post:**
```bash
curl -X DELETE http://localhost:5001/api/timeline_post/1
```

## 🧪 Testing

### Automated API Testing

Run the comprehensive test suite to verify all API endpoints:

```bash
./curl-test.sh
```

This script will:
- ✅ Check server connectivity
- ✅ Test GET endpoint (retrieve posts)
- ✅ Test POST endpoint (create posts)
- ✅ Test DELETE endpoint (remove posts)
- ✅ Verify data persistence
- ✅ Clean up test data automatically

### Manual Testing

You can also test individual endpoints manually:

```bash
# Test server is running
curl http://localhost:5001/api/timeline_post

# Create a test post
curl -X POST http://localhost:5001/api/timeline_post \
  -d "name=Test User" \
  -d "email=test@example.com" \
  -d "content=Test message"

# Delete a post (replace 1 with actual post ID)
curl -X DELETE http://localhost:5001/api/timeline_post/1
```

## 📁 Project Structure

```
Ebuka-Salim-Portfolio/
├── app/
│   ├── __init__.py          # Main Flask application
│   ├── static/              # CSS, images, and static files
│   ├── templates/           # HTML templates
│   └── markers.json         # Travel map markers data
├── .venv/                   # Virtual environment
├── start_server.sh          # Server startup script
├── curl-test.sh            # API testing script
├── requirements.txt         # Python dependencies
├── example.env             # Environment template
└── README.md               # This file
```

## 🔧 Development

### Database Models

**TimelinePost Model:**
- `id` (Integer, Primary Key)
- `name` (String, Required)
- `email` (String, Required)
- `content` (Text, Required)
- `created_at` (DateTime, Auto-generated)

### Adding New Features

1. Create a new branch for your feature
2. Implement your changes
3. Test using the provided testing scripts
4. Update documentation as needed
5. Submit a pull request

### Troubleshooting

**Port 5000 in use?** 
- macOS often uses port 5000 for AirTunes
- The app is configured to use port 5001 instead
- If needed, change the port in `start_server.sh`

**Database connection issues?**
- Verify MySQL is running: `brew services start mysql` (macOS)
- Check your `.env` file credentials
- Ensure the database exists

**Import errors?**
- Activate your virtual environment: `source .venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt` 

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

### Development Workflow
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`./curl-test.sh`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Code Standards
- Follow PEP 8 style guidelines for Python
- Add comments for complex logic
- Update tests when adding new API endpoints
- Update documentation for new features

## 📝 License

This project is part of the MLH Fellowship program.

## 🎯 Future Enhancements

- [ ] Add user authentication
- [ ] Implement timeline post editing (PUT endpoint)
- [ ] Add pagination for timeline posts
- [ ] Create frontend interface for timeline posts
- [ ] Add image uploads for timeline posts
- [ ] Implement search functionality
- [ ] Add API rate limiting
- [ ] Create admin dashboard

---

**Happy coding!** 🚀
