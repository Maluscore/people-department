from . import db
from . import ModelMixin
from . import timestamp



class Tweet(db.Model, ModelMixin):
    __tablename__ = 'tweets'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    created_time = db.Column(db.Integer, default=0)
    com_count = db.Column(db.Integer, default=0)
    deleted = db.Column(db.Integer, default=0)
    sender_name = db.Column(db.String())
    comments = db.relationship('Comment')
    likes = db.relationship('Like', lazy='dynamic')
    # 这是一个外键
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, form):
        self.content = form.get('content', '')
        self.created_time = timestamp()
        self.deleted = 0

    def json(self):
        self.id  # 加上这个就可以了
        _dict = self.__dict__.copy()
        d = {k: v for k, v in _dict.items() if k not in self.blacklist()}
        return d

    def blacklist(self):
        b = [
            '_sa_instance_state',
        ]
        return b

    def likes_count(self):
        num = self.likes.count()
        return num

    def users_id(self):
        all_likes = self.likes.all()
        return [a.user_id for a in all_likes]

    def update(self, form):
        self.content = form.get('content', '')
        self.created_time = timestamp()
        return True
