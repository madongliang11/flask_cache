from flask import Flask


from apps.ext import init_db, init_ext


# 入口函数
from apps.main.views import main
from apps.upfile.views import upload


def create_app():
    app = Flask(__name__)
    # 配置密钥
    app.config['SECRET_KEY']='123456'
    app.debug = True
    # 注册蓝图
    register(app)
    # 初始化数据库相关配置
    init_ext(app)
    return app


# 注册蓝图对象
def register(app:Flask):
    app.register_blueprint(main)
    app.register_blueprint(upload)


