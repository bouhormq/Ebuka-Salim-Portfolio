import unittest
from peewee import *

from app import TimelinePost
from playhouse.shortcuts import model_to_dict

MODELS = [TimelinePost]

test_db = SqliteDatabase(':memory:')

class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)

        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        test_db.drop_tables(MODELS)

        test_db.close()
    
    def test_timeline_post(self):
        first_post = TimelinePost.create(name="John Doe", email = "john@example.com", content="Hello world, I\'m John!")
        assert first_post.id == 1
        second_post = TimelinePost.create(name="Jane Doe", email = "jane@example.com", content="Hello world, I\'m Jane!")
        assert second_post.id == 2

        posts = TimelinePost.select().order_by(TimelinePost.id)
        assert [model_to_dict(posts[1])[key] for key in ['id', 'name', 'email', 'content']] == [2,'Jane Doe', 'jane@example.com', "Hello world, I'm Jane!"]
        assert [model_to_dict(posts[0])[key] for key in ['id', 'name', 'email', 'content']] == [1,'John Doe', 'john@example.com', "Hello world, I'm John!"]