import unittest
import os
os.environ['TESTING'] = 'true'

from app import app, init_database, mydb as app_mydb

class AppTestCase(unittest.TestCase):
    def setUp(self):
        # Set up a new app instance for each test
        os.environ['TESTING'] = 'true'
        global mydb
        mydb = app_mydb
        self.client = app.test_client()
        init_database()

    def tearDown(self):
        # Drop all tables to ensure a clean state for the next test
        from app import TimelinePost
        mydb.drop_tables([TimelinePost])
        # Close the database connection after each test
        if not mydb.is_closed():
            mydb.close()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)

        nav_links = [
            '<li><a href="/">Home</a></li>',
            '<li><a href="/about">About</a></li>',
            '<li><a href="/work">Work</a></li>',
            '<li><a href="/education">Education</a></li>',
            '<li><a href="/hobbies">Hobbies</a></li>',
            '<li><a href="/travel">Travel</a></li>',
            '<li><a href="/timeline">Timeline</a></li>'
        ]
        for link in nav_links:
            assert link in html

        assert "<title>MLH Fellow</title>" in html
        assert "<img src=\"/static/img/logo.jpg\">" in html
        assert "<h1>MLH Fellow</h1>" in html
    
    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0

        post_response = self.client.post('/api/timeline_post', data={
                            'name': 'Test User',
                            'email': 'test@example.com',
                            'content': 'This is a test timeline post'
        })
        assert post_response.status_code == 200
        assert post_response.is_json
        post_json = post_response.get_json()
        assert post_json["name"] == 'Test User'
        assert post_json["email"] == 'test@example.com'
        assert post_json["content"] == 'This is a test timeline post'

        get_response = self.client.get("/api/timeline_post")
        assert get_response.status_code == 200
        assert get_response.is_json
        get_json = get_response.get_json()
        assert "timeline_posts" in json
        assert len(get_json["timeline_posts"]) == 1
        
        page_response = self.client.get("/timeline")
        assert page_response.status_code == 200
        html = page_response.get_data(as_text=True)

        nav_links = [
            '<li><a href="/">Home</a></li>',
            '<li><a href="/about">About</a></li>',
            '<li><a href="/work">Work</a></li>',
            '<li><a href="/education">Education</a></li>',
            '<li><a href="/hobbies">Hobbies</a></li>',
            '<li><a href="/travel">Travel</a></li>',
            '<li><a href="/timeline">Timeline</a></li>'
        ]
        for link in nav_links:
            assert link in html

        assert "<title>Timeline</title>" in html
        assert "<h3>This is a test timeline post - July 17, 2025</h3>", "<p>test@example.com</p>" in html

    def test_malformed_timeline_post(self):
        response = self.client.post("/api/timeline_post", data=
                                    {
                                        "email": "john@example.com",
                                        "content": "Hello world, I'm John!"
                                    })
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        response = self.client.post("/api/timeline_post", data=
                                    {
                                        "name": "John Doe",
                                        "email": "john@example.com",
                                        "content": ""
                                    })
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        response = self.client.post("/api/timeline_post", data=
                                    {
                                        "name": "John Doe",
                                        "email": "not-an-email",
                                        "content": "Hello world, I'm John!"
                                    })
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html