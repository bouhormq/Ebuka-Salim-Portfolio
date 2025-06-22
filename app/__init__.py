import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify, url_for, redirect
from dotenv import load_dotenv
import logging

load_dotenv()
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

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
    return render_template('travel.html', title="Travel", url=os.getenv("URL"), markers=markers)


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
