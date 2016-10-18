from routes import *

main = Blueprint('auth', __name__)


@main.route('/')
def index():
    view = 'auth.login_view'
    # 由于是在相同蓝图下, 所以也可以这样写, 省略前缀
    # view = '.login_view'
    return redirect(url_for(view))


# 显示登录界面的函数  GET
@main.route('/login')
def login_view():
    return render_template('login.html')


@main.route('/register', methods=['POST'])
def register():
    print('register')
    form = request.get_json()
    log('form is ', form)
    u = User(form)
    print('register 2')
    r = {
        'success': True
    }
    status, msgs = u.register_validate()
    if status:
        print("register success", form)
        # 保存到数据库
        u.gid = 10
        u.save()
        r['next'] = request.args.get('next', url_for('user.timeline_view', user_id=u.id))
        session.permanent = True
        session['username'] = u.username
        session['user_id'] = u.id
    else:
        print('register failed', form)
        r['success'] = False
        r['message'] = '\n'.join(msgs)
    return jsonify(r)


# 处理登录请求  POST
@main.route('/login', methods=['POST'])
def login():
    form = request.get_json()
    username = form.get('username', '')
    user = User.user_by_name(username)

    print('user login', user, form)
    r = {
        'success': False,
        'message': '登录失败',
    }
    if user is not None and user.validate_auth(form):
        r['success'] = True
        r['next'] = request.args.get('next', url_for('user.timeline_view', user_id=user.id))
        session.permanent = True
        session['username'] = username
        session['user_id'] = user.id
    else:
        r['success'] = False
        r['message'] = '登录失败'
    log('登录成功')
    return jsonify(r)


# 处理注销请求 POST
@main.route('/logoff')
@login_required
def logoff():
    session.pop('username')
    session.pop('user_id')
    return redirect(url_for('.login_view'))
