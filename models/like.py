from . import db
from . import ModelMixin
from . import timestamp

# 建立多对多的关系

class Like(db.Model, ModelMixin):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True)
    created_time = db.Column(db.Integer, default=0)
    tweet_id = db.Column(db.Integer, db.ForeignKey('tweets.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    users = db.relationship('User')

    def __init__(self):
        self.created_time = timestamp()
