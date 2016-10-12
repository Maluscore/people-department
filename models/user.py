from . import ModelMixin
from . import db
from . import timestamp


class User(db.Model, ModelMixin):
    # 类的属性就是数据库表的字段
    # 这些都是内置的 __tablename__ 是表名
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    created_time = db.Column(db.Integer, default=0)
    deleted = db.Column(db.Integer, default=0)
    tweets = db.relationship('tweet', backref='user')

    # 这是引用别的表的数据的属性，表明了它关联的东西
    # tweets = db.relationship('Tweet', backref='user')

    @staticmethod
    def user_by_name(username):
        return User.query.filter_by(username=username).first()

    def __init__(self, form):
        super(User, self).__init__()
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.created_time = timestamp()
        self.deleted = 0

    def json(self):
        # 加上这个就可以了
        self.id
        _dict = self.__dict__.copy()
        d = {k: v for k, v in _dict.items() if k not in self.blacklist()}
        # d['topics'] = [t.json() for t in self.topics]
        print('debug d, ', d)
        return d

    def blacklist(self):
        b = [
            'password',
            'created_time',
            'id',
            '_sa_instance_state',
        ]
        return b

    def validate_auth(self, form):
        username = form.get('username', '')
        password = form.get('password', '')
        username_equals = self.username == username
        password_equals = self.password == password
        return username_equals and password_equals

    def update(self, form):
        print('user.update, ', form)
        self.password = form.get('password', self.password)

    # 验证注册用户的合法性
    def register_validate(self):
        min_len = 3
        valid_username = User.query.filter_by(username=self.username).first() == None
        valid_username_len = len(self.username) >= min_len
        valid_password_len = len(self.password) >= min_len
        msgs = []
        if not valid_username:
            message = '用户名已经存在'
            msgs.append(message)
        elif not valid_username_len:
            message = '用户名长度必须大于等于 3'
            msgs.append(message)
        elif not valid_password_len:
            message = '密码长度必须大于等于 3'
            msgs.append(message)
        status = valid_username and valid_username_len and valid_password_len
        return status, msgs
