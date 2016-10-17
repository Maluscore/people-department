from routes import *
from models.follow import Follow

main = Blueprint('user', __name__)


@main.route('/timeline/<int:user_id>')
@login_required
def timeline_view(user_id):
    u = User.query.filter_by(id=user_id).first_or_404()
    log('u is ,', u)
    follow_count = Follow.follow_count(u.id)
    fans = Follow.fans(u.id)
    tweets = [t for t in u.tweets if t.deleted == 0]
    t_length = len(tweets)
    # print('debug t,', tweets)
    all_follows = []
    for i in follow_count:
        all_follows.append(User.query.filter_by(id=i).first())
    all_follow_tweets = []
    for i in all_follows:
        all_follow_tweets.extend(i.tweets)
    follow_tweets = [t for t in all_follow_tweets if t.deleted == 0]
    show_tweets = tweets + follow_tweets
    show_tweets.sort(key=lambda t: t.created_time, reverse=True)
    d = dict(
        t_length=t_length,
        login_id=session['user_id'],
        current_user=u,
        tweets=show_tweets,
        follows_count=len(follow_count),
        fans_count=len(fans),
    )
    return render_template('timeline.html', **d)


@main.route('/all/<int:user_id>')
@login_required
def user_all(user_id):
    users = User.query.all()
    user = current_user()
    follow_count = Follow.follow_count(user.id)
    fans = Follow.fans(user.id)
    u = User.query.filter_by(id=user_id).first_or_404()
    tweets = [t for t in u.tweets if t.deleted == 0]
    t_length = len(tweets)
    d = dict(
        user_all=users,
        current_user=user,
        login_id=user_id,
        follows_count=len(follow_count),
        fans_count=len(fans),
        t_length=t_length,
    )
    return render_template('users_list.html', **d)


# @main.route('/<user_id>')
# @login_required
# def user_view(user_id):
#     u = User.query.filter_by(id=user_id).first()
#     user = current_user()
#     follow_list = Follow.follow_count(user.id)
#     if u.id in follow_list:
#         status = '取消关注'
#     elif u.id not in follow_list and u.id != user.id:
#         status = '关注'
#     else:
#         status = ''
#     follow_count = Follow.follow_count(u.id)
#     fans = Follow.fans(u.id)
#     tweets = [t for t in u.tweets if t.deleted == 0]
#     d = dict(
#         user=u,
#         tweets=tweets,
#         current_user=user,
#         status=status,
#         follows_count=len(follow_count),
#         fans_count=len(fans),
#     )
#     return render_template('user.html', **d)


# @main.route('/weibo/<int:user_id>', methods=['POST'])
# @login_required
# def weibo_display(user_id):
#     u = User.query.filter_by(id=user_id).first()
#     tweets = u.tweets
#     tweets.sort(key=lambda t: t.created_time, reverse=True)
#     all_t = []
#     for t in tweets:
#         item = t.json()
#         item['likes_count'] = t.likes_count()
#         all_t.append(item)
#     log('灌水成功')
#     r = dict(
#         message='加载成功!',
#         success=True,
#         data=all_t,
#     )
#     return jsonify(r)


@main.route('/profile/<int:user_id>', methods=['POST'])
@login_required
def profile_alloc(user_id):
    r = dict(
        message='跳转成功',
        success=True,
        next='/user/profile/{}'.format(user_id)
    )
    return jsonify(r)


@main.route('/profile/<int:user_id>')
@login_required
def profile_view(user_id):
    u = User.query.filter_by(id=user_id).first_or_404()
    follow_count = Follow.follow_count(u.id)
    fans = Follow.fans(u.id)
    tweets = [t for t in u.tweets if t.deleted == 0]
    t_length = len(tweets)
    # print('debug t,', tweets)
    all_follows = []
    for i in follow_count:
        all_follows.append(User.query.filter_by(id=i).first())
    all_follow_tweets = []
    for i in all_follows:
        all_follow_tweets += i.tweets
    tweets.sort(key=lambda t: t.created_time, reverse=True)
    login_id = session['user_id']
    if u.id in Follow.follow_count(login_id):
        status = '取消关注'
    else:
        status = '关注'
    d = dict(
        t_length=t_length,
        current_user=u,
        login_id=login_id,
        tweets=tweets,
        follows_count=len(follow_count),
        fans_count=len(fans),
        status=status,
    )
    return render_template('user_profile.html', **d)


@main.route('/follow/list/<int:user_id>', methods=['POST'])
@login_required
def following_alloc(user_id):
    r = dict(
        message='跳转成功',
        success=True,
        next='/user/follow/list/{}'.format(user_id)
    )
    return jsonify(r)


# 显示 关注列表 的界面 GET
@main.route('/follow/list/<int:user_id>')
@login_required
def following_view(user_id):
    u = User.query.filter_by(id=user_id).first_or_404()
    follow_count = Follow.follow_count(u.id)
    fans = Follow.fans(u.id)
    tweets = [t for t in u.tweets if t.deleted == 0]
    t_length = len(tweets)
    # print('debug t,', tweets)
    all_follows = []
    for i in follow_count:
        all_follows.append(User.query.filter_by(id=i).first())
    login_id = session['user_id']
    if u.id in Follow.follow_count(login_id):
        status = '取消关注'
    else:
        status = '关注'
    d = dict(
        t_length=t_length,
        current_user=u,
        login_id=login_id,
        follows_count=len(follow_count),
        fans_count=len(fans),
        status=status,
        following=all_follows,
    )
    return render_template('follow_list.html', **d)


@main.route('/fan/list/<int:user_id>', methods=['POST'])
@login_required
def fan_alloc(user_id):
    r = dict(
        message='跳转成功',
        success=True,
        next='/user/fan/list/{}'.format(user_id)
    )
    return jsonify(r)


# 显示 粉丝列表 的界面 GET
@main.route('/fan/list/<user_id>')
@login_required
def fan_view(user_id):
    u = User.query.filter_by(id=user_id).first_or_404()
    follow_count = Follow.follow_count(u.id)
    all_fans = Follow.fans(user_id)
    tweets = [t for t in u.tweets if t.deleted == 0]
    t_length = len(tweets)
    login_id = session['user_id']
    if u.id in Follow.follow_count(login_id):
        status = '取消关注'
    else:
        status = '关注'
    all_fans.sort(key=lambda t: t.created_time, reverse=True)
    d = dict(
        t_length=t_length,
        current_user=u,
        login_id=login_id,
        follows_count=len(follow_count),
        fans_count=len(all_fans),
        status=status,
        all_fans=all_fans,
    )
    return render_template('fans_list.html', **d)


# 处理 关注用户 的请求
@main.route('/follow', methods=['POST'])
def follow_act():
    form = request.get_json()
    user_now = current_user()
    f = Follow()
    f.user_id = user_now.id
    f.followed_id = form['id']
    f.save()
    r = {
        'success': True,
        'message': '关注成功！'
    }
    print('debug, ', r['message'])
    return jsonify(r)


# 处理 取消关注 的请求
@main.route('/unfollow', methods=['POST'])
def unfollow_act():
    form = request.get_json()
    user_id = form['id']
    user_now = current_user()
    f = Follow().query.filter_by(user_id=user_now.id, followed_id=user_id).first()
    f.delete()
    r = {
        'success': True,
        'message': '取消关注成功！'
    }
    print('debug, ', r['message'])
    return jsonify(r)

