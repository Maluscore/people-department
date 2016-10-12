from routes import *
from models.follow import Follow

main = Blueprint('user', __name__)


@main.route('/timeline/<int:user_id>')
@login_required
def timeline_view(user_id):
    u = User.query.filter_by(id=user_id).first_or_404()
    follow_count = Follow.follow_count(u.id)
    fans = Follow.fans(u.id)
    tweets = [t for t in u.tweets if t.deleted == 0]
    # print('debug t,', tweets)
    all_follows = []
    for i in follow_count:
        all_follows.append(User.query.filter_by(id=i).first())
    all_follow_tweets = []
    for i in all_follows:
        all_follow_tweets += i.tweets
    follow_tweets = [t for t in all_follow_tweets if t.deleted == 0]
    show_tweets = tweets + follow_tweets
    show_tweets.sort(key=lambda t: t.created_time, reverse=True)
    d = dict(
        current_user=u,
        tweets=show_tweets,
        follows_count=len(follow_count),
        fans_count=len(fans),
    )
    return render_template('timeline.html', **d)


@main.route('/user/all')
@login_required
def user_all():
    users = User.query.all()
    user = current_user()
    follow_count = Follow.follow_count(user.id)
    fans = Follow.fans(user.id)
    d = dict(
        user_all=users,
        current_user=user,
        follows_count=len(follow_count),
        fans_count=len(fans),
    )
    return render_template('user_all.html', **d)


@main.route('/user/<user_id>')
@login_required
def user_view(user_id):
    u = User.query.filter_by(id=user_id).first()
    user = current_user()
    follow_list = Follow.follow_count(user.id)
    if u.id in follow_list:
        status = '取消关注'
    elif u.id not in follow_list and u.id != user.id:
        status = '关注'
    else:
        status = ''
    follow_count = Follow.follow_count(u.id)
    fans = Follow.fans(u.id)
    tweets = [t for t in u.tweets if t.deleted == 0]
    d = dict(
        user=u,
        tweets=tweets,
        current_user=user,
        status=status,
        follows_count=len(follow_count),
        fans_count=len(fans),
    )
    return render_template('user.html', **d)


# 显示 关注列表 的界面 GET
@main.route('/follow/list/<user_id>')
@login_required
def follow_view(user_id):
    user_now = current_user()
    user = User.query.filter_by(id=user_id).first()
    follow_count = Follow.follow_count(user.id)
    fans = Follow.fans(user.id)
    follow_id = Follow.follow_count(user_id)
    follow_users = []
    for i in follow_id:
        follow_users.append(User.query.filter_by(id=i).first())
    follow_users.sort(key=lambda t: t.created_time, reverse=True)
    d = dict(
        current_user=user_now,
        all_follows=follow_users,
        user=user,
        follows_count=len(follow_count),
        fans_count=len(fans),
    )
    return render_template('follow_users.html', **d)


# 显示 粉丝列表 的界面 GET
@main.route('/fan/list/<user_id>')
@login_required
def fan_view(user_id):
    user_now = current_user()
    user = User.query.filter_by(id=user_id).first()
    all_fans = Follow.fans(user_id)
    follow_count = Follow.follow_count(user_id)
    all_fans.sort(key=lambda t: t.created_time, reverse=True)
    d = dict(
        current_user=user_now,
        all_fans=all_fans,
        user=user,
        follows_count=len(follow_count),
        fans_count=len(all_fans),
    )
    return render_template('fan_users.html', **d)


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
    # return redirect(url_for('timeline_view', username=u.username))


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
    # return redirect(url_for('timeline_view', username=u.username))
