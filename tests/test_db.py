import os
import unittest
from peewee import *
from playhouse.shortcuts import model_to_dict

from app import init_database, mydb as app_mydb

from app import TimelinePost

MODELS = [TimelinePost]

test_db = SqliteDatabase(':memory:')

class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        # Set up a new app instance for each test
        os.environ['TESTING'] = 'true'
        global mydb
        mydb = app_mydb
        init_database()

    def tearDown(self):
        # Drop all tables to ensure a clean state for the next test
        from app import TimelinePost
        mydb.drop_tables([TimelinePost])
        # Close the database connection after each test
        if not mydb.is_closed():
            mydb.close()

    def test_timeline_post(self):
        from app import TimelinePost
        # Create a new timeline post
        first_post = TimelinePost.create(name='John Doe', email='john@example.com', content='Hello world, I\'m John!')
        self.assertEqual(first_post.id, 1)
        second_post = TimelinePost.create(name='Jane Doe', email='jane@example.com', content='Hello world, I\'m Jane!')
        self.assertEqual(second_post.id, 2)
        
        # Get all timeline posts
        timeline_posts = [model_to_dict(p) for p in TimelinePost.select()]
        self.assertEqual(len(timeline_posts), 2)
        self.assertEqual(timeline_posts[0]['name'], 'John Doe')
        self.assertEqual(timeline_posts[1]['name'], 'Jane Doe')