from flask import (
	render_template,
	request,
	redirect,
	session,
	url_for,
	Blueprint,
	make_response,
)

from models.user import User

from utils import log

main = Blueprint('index', __name__)


def current_user():
	# 从 session 中找到 user_id 字段, 找不到就 -1
	# 然后 User.find_by 来用 id 找用户
	# 找不到就返回 None
	uid = session.get('user_id', -1)
	u = User.find_by(id=uid)
	return u


"""
用户在这里可以
    访问首页
    注册
    登录

用户登录后, 会写入 session, 并且定向到 /profile
"""


# index主页面
@main.route("/", methods=[ 'GET' ])
def index():
	u = current_user()
	login = request.args.get('msg', None)
	if u is not None:
		print(u)
		return redirect(url_for('todo.index'))
	elif login == 'False':
		msg = '登录失败,请检查用户名或密码!'
		return render_template('login.html', msg=msg)
	else:
		return render_template('login.html')


# register登录页面
@main.route("/register", methods=[ 'GET' ])
def registered():
	return render_template('register.html')


# 注册
@main.route("/register", methods=[ 'POST' ])
def register():
	form = request.form
	# 用类函数来判断
	u = User.register(form)
	if u is None:
		msg = '注册失败,请检查!'
		return render_template('register.html', msg=msg)
	else:
		msg = '注册成功!'
		return render_template('register.html', user=u, msg=msg)


# 登录
@main.route("/login", methods=[ 'POST' ])
def login():
	form = request.form
	u = User.validate_login(form)
	if u is None:
		# 转到 topic.index 页面
		msg = 'False'
		return redirect(url_for('.index', msg=msg))
	# return render_template('login.html', msg=msg)
	else:
		# session 中写入 user_id
		session[ 'user_id' ] = u.id
		# 设置 cookie 有效期为 永久
		session.permanent = True
		return redirect(url_for('todo.index'))

@main.route("/logout")
def logout():
	session['user_id'] = None
	print('撒擦',session)
	return redirect(url_for('.index'))
