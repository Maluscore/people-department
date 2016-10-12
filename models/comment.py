from . import db
from . import ModelMixin
from . import timestamp


class Comment(db.Model, ModelMixin):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    created_time = db.Column(db.INTEGER, default=0)
    sender_name = db.Column(db.String())
    tweet_id = db.Column(db.Integer, db.ForeignKey('tweets.id'))

    def __init__(self, form):
        self.content = form.get('content', '')
        self.created_time = timestamp()

    def json(self):
        # Model 是延迟载入的, 如果没有引用过数据, 就不会从数据库中加载
        # 引用一下 id 这样数据就从数据库中载入了
        # 返回的json应该带一个type
        self.id
        d = {k: v for k, v in self.__dict__.items() if k not in self.blacklist()}
        d['type'] = 'Comment'
        d['created_time'] = self.created_time
        return d

    def blacklist(self):
        b = [
            '_sa_instance_state',
            'password',
            'id',
            'tweet_id',
        ]
        return b
