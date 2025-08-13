import os
from datetime import datetime
import datetime
from flask import Flask, render_template, request, jsonify, url_for, redirect
from dotenv import load_dotenv
import logging
import json
from peewee import *
from peewee import MySQLDatabase
from playhouse.shortcuts import model_to_dict 
import re

load_dotenv()
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Database initialization
mydb = None
database_connected = False

# Placeholder for TimelinePost Model (will be set later)
TimelinePost = None

def init_database():
    global mydb, database_connected, TimelinePost
    
    # Check for testing mode first
    if os.getenv("TESTING") == "true":
        print("Running in test mode")
        mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
    else:
        # Check if all required environment variables are present for production
        required_vars = ["MYSQL_DATABASE", "MYSQL_USER", "MYSQL_PASSWORD", "MYSQL_HOST"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            print(f"⚠️  Missing database environment variables: {', '.join(missing_vars)}")
            print("⚠️  Timeline posts will not work without database connection")
            database_connected = False
            return False
        
        mydb = MySQLDatabase(
            os.getenv("MYSQL_DATABASE"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            host=os.getenv("MYSQL_HOST"),
            port=int(os.getenv("MYSQL_PORT", 3306))
        )

    try:
        # Define TimelinePost Model after database is created
        class TimelinePost(Model):
            name = CharField()
            email = CharField()
            content = TextField()
            created_at = DateTimeField(default=datetime.datetime.now)
            
            class Meta:
                database = mydb
        
        # Make TimelinePost available globally
        globals()['TimelinePost'] = TimelinePost
        
        mydb.connect()
        mydb.create_tables([TimelinePost])
        database_connected = True
        print("✅ Database connected and tables created successfully")
        return True
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        print("⚠️  Timeline posts will not work without database connection")
        database_connected = False
        return False

# TimelinePost Model
class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        database = mydb

# Initialize database connection
init_database()

about_me = "This is sample text. You can click here and replace with actual content about yourself." 

work_experiences = [
    {
        "job_title": "Software Engineer",
        "company": "Tech Corp",
        "dates": "Jan 2022 - Present",
        "description": "Developing and maintaining web applications."
    },
    {
        "job_title": "Intern",
        "company": "Startup Inc.",
        "dates": "May 2021 - Aug 2021",
        "description": "Assisted with front-end development."
    }
]

education_history = [
    {
        "degree": "Bachelor of Science in Computer Science",
        "institution": "University of Technology",
        "years": "2021 - 2025"
    }
]

hobbies_data = [
    {
        "name": "Photography",
        "image": 'img/logo.jpg',
        "description": "Capturing moments and landscapes."
    },
    {
        "name": "Hiking",
        "image": 'img/logo.jpg',
        "description": "Exploring trails and nature."
    }
]

NAV_PAGES = [
    {'endpoint': 'index', 'name': 'Home'},
    {'endpoint': 'about', 'name': 'About'},
    {'endpoint': 'work', 'name': 'Work'},
    {'endpoint': 'education', 'name': 'Education'},
    {'endpoint': 'hobbies', 'name': 'Hobbies'},
    {'endpoint': 'travel', 'name': 'Travel'},
    {'endpoint': 'timeline', 'name': 'Timeline'},
]

@app.context_processor
def inject_nav_pages():
    return dict(nav_pages=NAV_PAGES)

@app.route('/')
def index():
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"))

@app.route('/about')
def about():
    return render_template('about.html', title="About Me", url=os.getenv("URL"), about_me=about_me)

@app.route('/save_about', methods=['POST'])
def save_about():
    global about_me
    about_me = request.form['about_me']
    return redirect(url_for('about'))

@app.route('/work')
def work():
    return render_template('work.html', title="Work Experience", url=os.getenv("URL"), work_experiences=work_experiences)

@app.route('/add_work', methods=['POST'])
def add_work():
    
    date1 = datetime.strptime(request.form['date1'], "%Y-%m-%d").strftime("%b %Y")
    date2 = datetime.strptime(request.form['date2'], "%Y-%m-%d").strftime("%b %Y")

    work_experiences.append({
        'job_title': request.form['job_title'],
        'company': request.form['company'],
        'dates': date1 + ' - ' + date2,
        'description': request.form['description']
    })
    return redirect(url_for('work'))

@app.route('/education')
def education():
    return render_template('education.html', title="Education", url=os.getenv("URL"), education_history=education_history)

@app.route('/add_education', methods=['POST'])
def add_education():
    
    year1 = datetime.strptime(request.form['year1'], "%Y-%m-%d").strftime("%Y")
    year2 = 'Present' if request.form.get('currently_attending') else datetime.strptime(request.form['year2'], "%Y-%m-%d").strftime("%Y")

    education_history.append({
        'degree': request.form['degree'],
        'institution': request.form['institution'],
        'years': year1 + ' - ' + year2
    })
    return redirect(url_for('education'))

@app.route('/hobbies')
def hobbies():
    # We need to generate the image URLs dynamically
    hobbies_with_urls = []
    for hobby in hobbies_data:
        hobbies_with_urls.append({
            'name': hobby['name'],
            'image': url_for('static', filename=hobby['image']),
            'description': hobby['description']
        })
    return render_template('hobbies.html', title="Hobbies", url=os.getenv("URL"), hobbies=hobbies_with_urls)

@app.route('/add_hobby', methods=['POST'])
def add_hobby():
    name = request.form['name']
    image_file = request.files['image']

    safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '_', '-')).rstrip().replace(' ', '_')
    filename = f"{safe_name}.jpg"
    upload_folder = os.path.join(app.static_folder, 'img')
    os.makedirs(upload_folder, exist_ok=True)
    save_path = os.path.join(upload_folder, filename)
    image_file.save(save_path)

    hobbies_data.append({
        'name': name,
        'image': f'img/{filename}',
        'description': request.form['description']
    })

    return redirect(url_for('hobbies'))

@app.route('/travel')
def travel():
    try:
        with open('app/markers.json', 'r') as f:
            markers = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        markers = []
    return render_template('travel.html', title="Travel", url=os.getenv("URL"), markers=markers)

@app.route('/add_marker', methods=['POST'])
def add_marker():
    data = request.get_json()
    if not data or 'lat' not in data or 'lng' not in data:
        return jsonify({'error': 'Invalid data'}), 400
    
    try:
        with open('app/markers.json', 'r') as f:
            markers = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        markers = []

    markers.append({
        'lat': data['lat'],
        'lng': data['lng'],
        'note': data.get('note', '')
    })

    with open('app/markers.json', 'w') as f:
        json.dump(markers, f, indent=4)

    return jsonify({'success': 'Marker added'}), 201


@app.route('/timeline')
def timeline():
    return render_template('timeline.html', title="Timeline", url=os.getenv("URL"))


@app.route('/upload', methods=['POST'])
def upload_file():
    app.logger.info("Upload endpoint was hit")
    if 'profile_picture' not in request.files:
        app.logger.error("No 'profile_picture' in request.files")
        return jsonify({'error': 'No file part'}), 400
    file = request.files['profile_picture']
    if file.filename == '':
        app.logger.error("Filename is empty")
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filename = 'logo.jpg'
        upload_folder = os.path.join(app.static_folder, 'img')
        save_path = os.path.join(upload_folder, filename)
        app.logger.info(f"Attempting to save file to: {save_path}")
        try:
            file.save(save_path)
            app.logger.info(f"Successfully saved file to: {save_path}")
            response = jsonify({'success': 'File uploaded successfully'})
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            return response, 200
        except Exception as e:
            app.logger.error(f"Failed to save file: {e}")
            return jsonify({'error': str(e)}), 500


# Timeline Post API Endpoints
@app.route('/api/timeline_post', methods=['POST'])
def post_timeline_post():
    if not database_connected:
        return jsonify({'error': 'Database not available'}), 503
    
    try:
        name = request.form['name']
        if name.strip() == "":
            return "Invalid name", 400
    except Exception as e:
        app.logger.error(f"Error creating timeline post: {e}")
        return "Invalid name", 400
    
    try:
        email = request.form['email']
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, email):
            return "Invalid email format", 400
    except Exception as e:
        app.logger.error(f"Error creating timeline post: {e}")
        return "Invalid email", 400
    
    try:
        content = request.form['content']
        if content.strip() == "":
            return "Invalid content", 400
    except Exception as e:
        app.logger.error(f"Error creating timeline post: {e}")
        return "Invalid content", 400
        
    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    return jsonify(model_to_dict(timeline_post))
    

@app.route('/api/timeline_post', methods=['GET'])
def get_timeline_post():
    if not database_connected:
        return jsonify({'error': 'Database not available', 'timeline_posts': []}), 503
    
    try:
        return jsonify({
            'timeline_posts': [
                model_to_dict(p) 
                for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
            ]
        })
    except Exception as e:
        app.logger.error(f"Error retrieving timeline posts: {e}")
        return jsonify({'error': str(e), 'timeline_posts': []}), 500

@app.route('/api/timeline_post/<int:post_id>', methods=['DELETE'])
def delete_timeline_post(post_id):
    if not database_connected:
        return jsonify({'error': 'Database not available'}), 503
    
    try:
        post = TimelinePost.get_by_id(post_id)
        post.delete_instance()
        return jsonify({'success': f'Timeline post {post_id} deleted successfully'}), 200
    except TimelinePost.DoesNotExist:
        return jsonify({'error': f'Timeline post {post_id} not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # For development only
    app.run(debug=True, host='0.0.0.0', port=5000)
