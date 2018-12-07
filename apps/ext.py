import datetime
import os

from flask import Flask
from flask_caching import Cache
from flask_login import LoginManager

# 初始化第三方插件
def init_ext(app):
    # 初始化session
    init_session(app)
    # 初始化cookies
    init_cookies(app)
    # 初始化数据库
    init_db(app)
    init_login(app)
    # 初始化缓存
    init_caching(app)
    # 初始化文件上传
    init_upload(app)

# 初始化数据库操作
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
def init_db(app):
    #dialect+driver://username:password@host:port/database
    app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@127.0.0.1:3306/flask_cache?charset=utf8'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # 打印sql语句
    app.config['SQLALCHEMY_ECHO']=True
    # 自动提交事物
    # app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
    db.init_app(app=app)
    migrate.init_app(app,db)

#   实例化登录对象
lm = LoginManager()

def init_login(app:Flask):
    lm.login_view = '/login/'
    # basic strong None
    lm.session_protection = 'strong'
    lm.init_app(app)

# 其他配置
'''
session 存储位置  
cookies
'''


'''
CACHE_DEFAULT_TIMEOUT 连接redis超时时间
CACHE_KEY_PREFIX redis缓存key的前缀
CACHE_REDIS_HOST  ip
CACHE_REDIS_PORT   端口
CACHE_REDIS_PASSWORD    密码
CACHE_REDIS_DB   数据库名
CACHE_ARGS
CACHE_OPTIONS
CACHE_REDIS_URL
'''




# 配置session
def init_session(app:Flask):
    # 配置加密session数据的密钥
    app.config['SECRET_KEY'] = 'sasadsd'
    # 表示使用session来存储session数据
    app.config['SESSION_TYPE']='redis'
    # 设置session的过期时间，默认关闭浏览器session失效
    app.config['PERMANENT_SEFETIME']= datetime.timedelta(days=7)

'''
cookie包含
键
值
过期时间 expires
限制
路径 path='/' 指定那个url可以访问到cookie；‘/’是所有； path='/'**
域名 domain=None（None代表当前域名）
secure=False  https安全相关
httponly  值应用于http传输，JavaScript无法获取

'''
def init_cookies(app:Flask):
    app.config['REMEMBER_COOKIE_NAME'] = ''
    # 默认是365天  时间对象
    app.config['REMEMBER_COOKIE_DUTATION'] = datetime.timedelta(days=7)
    app.config['REMEMBER_COOKIE_PATH']='/'
    # 配置子域名
    #app.config['REMEMBER_COOKIE_DOMAIN']='.baidu.com'
    # app.config['REMEMBER_COOKIE_HTTPONLY']=True

# 缓存
cache = Cache()
CACHE_CONFIG = {
    'CACHE_TYPE':'redis',
    'CACHE_REDIS_HOST':'127.0.0.1',
    'CACHE_REDIS_PORT':'6379',
    'CACHE_REDIS_DB':'1'
}
def init_caching(app:Flask):
    cache.init_app(app,config=CACHE_CONFIG)


'''
文件上传配置
pip install flask-uploads
1、必须是post请求 必须是form-data格式
2、UploadSet文件上传的核心对象
'''
from flask_uploads import UploadSet, IMAGES, DOCUMENTS, configure_uploads, patch_request_class

# media
'''
参数说明
name 上传文件的子目录，默认名为files
extensions 上传文件的类型（扩展名），默认是TEXT，DOCUMENTS，IMAGES， DATA
default_dest 配置文件上传的根目录 例如：H:\flask\flask_cache\apps\media
'''
# 实例化对象
# 上传图片
img_set = UploadSet(name='images',extensions=IMAGES)
# 上传文档文件
doc_set = UploadSet(name='doc',extensions=DOCUMENTS)


'''
不能通过flask对象.init_app与flask对象关联
通过configure_uploads初始化UploadSet对象
'''
# __file__获取当前文件的路径
# 配置文件上传的根目录
BASE_DIR=os.path.dirname(__file__)
UPLOAD_ROOT_PATH=os.path.join(BASE_DIR,'static/upload')
def init_upload(app:Flask):
    # 配置根目录
    app.config['UPLOADS_DEFAULT_DEST']=UPLOAD_ROOT_PATH
    # 配置文件上传的最大长度
    app.config['MAX_CONTENT_LENGTH']=10*1024*1024
    # 生成图片的url地址 默认xxx/_uploads/images/user/1/30cbcf2c2d.jpg
    app.config['UPLOADS_DEFAULT_URL']='/static/upload/'
    # 初始化img_set
    configure_uploads(app,img_set)
    # size=10*1024*1024等价于app.config['MAX_CONTENT_LENGTH']=10*1024*1024
    # patch_request_class(app,size=10*1024*1024)
    configure_uploads(app, doc_set)