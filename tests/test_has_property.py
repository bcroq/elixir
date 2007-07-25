"""
    simple test case
"""

from sqlalchemy import column_property
from elixir import *

def setup():
    metadata.connect('sqlite:///')

def teardown():
    cleanup_all()


class TestHasProperty(object):
    def teardown(self):
        objectstore.clear()
    
    def test_has_property(self):
        global Tag, User

        class Tag(Entity):
            has_field('score1', Float)
            has_field('score2', Float)
            has_property('query_score', 
                         lambda c: column_property(
                             (c.score1 * c.score2).label('query_score')))

            belongs_to('user', of_kind='User')

            @property
            def prop_score(self):
                return self.score1 * self.score2

        class User(Entity):
            has_field('name', String(16))
            has_many('tags', of_kind='Tag', lazy=False) 

        create_all()

        u1 = User(name='joe', tags=[Tag(score1=5.0, score2=3.0), 
                                    Tag(score1=55.0, score2=1.0)])

        u2 = User(name='bar', tags=[Tag(score1=5.0, score2=4.0), 
                                    Tag(score1=50.0, score2=1.0),
                                    Tag(score1=15.0, score2=2.0)])

        objectstore.flush()
        objectstore.clear()
        
        for user in User.q:
            for tag in user.tags:
                assert tag.query_score == tag.prop_score

