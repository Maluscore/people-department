from . import db
from . import ModelMixin
from . import timestamp


class Follow(db.Model, ModelMixin):
    __tablename__ = 'follows'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    followed_id = db.Column(db.Integer)
    created_time = db.Column(db.Integer, default=0)
    # 关注了哪些用户，配合user_id使用
    follows = db.relationship('User')
    # 有哪些粉丝，配合followed_id使用
    # fans = db.relationship('User')

    def __init__(self):
        self.created_time = timestamp()

    @staticmethod
    def follow_count(user_id):
        f = Follow.query.filter_by(user_id=user_id).all()
        return [x.followed_id for x in f]

    @staticmethod
    def fans(user_id):
        f = Follow.query.filter_by(followed_id=user_id).all()
        fan_list = [x.follows for x in f]
        return fan_list
