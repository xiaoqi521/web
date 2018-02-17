from models import Model


# 定义User类
class User(Model):
	"""
	初始化User类
	User 是一个保存用户数据的 model
	现在有id、 username、 password
	"""
	def __init__(self, form):
		self.id = form.get('id', None)
		self.username = form.get('username', '')
		self.password = form.get('password', '')

	# 加密password
	def salted_password(self, password, salt='sc^$%#%7fgeagqergh'):
		import hashlib
		def sha256(asscii_str):
			return hashlib.sha256(asscii_str.encode('ascii')).hexdigest()
		hash1 = sha256(password)
		hash2 = sha256(hash1 + salt)
		return hash2

	def hashed_password(self, pwd):
		import hashlib
		# 用ascii 编码转换成 bytes 对象
		p = pwd.encode('ascii')
		s = hashlib.sha256(p)
		# 返回摘要字符串
		return s.hexdigest()

	# 类方法 注册
	@classmethod
	def register(cls, form):
		name = form.get('username', '')
		pwd = form.get('password', '')
		# 用户名长度判断、用户名是否已经存在 TODO：（应该分开写）
		if len(name) > 2 and User.find_by(username=name) is None:
			u = User.new(form)
			# 在此加密密码
			u.password = u.salted_password(pwd)
			# 保存user
			u.save()
			return u
		else:
			return None

	# 验证登录
	@classmethod
	def validate_login(cls, form):
		u = User(form)
		user = User.find_by(username=u.username)
		if user is not None and user.password == u.salted_password(u.password):
			return user
		else:
			return None


