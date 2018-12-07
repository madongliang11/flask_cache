import datetime
import random

from flask import Blueprint, render_template

from apps.account.models import User
from apps.config import BlueKeyConfig
from apps.ext import cache

main = Blueprint(BlueKeyConfig.BLUEPRINT_MAIN_KEY,__name__)

'''
缓存的使用
1、在views使用
    使用装饰器
    @cache.cached（）
    @cache.memoize（）
2、在模板中使用（必须要写过时时间）
    {% cache 过时时间 %}
        内容
    {% endcache %}
'''

# 注意：缓存装饰器尽量写在蓝图下面
'''
参数
timeout 单位是秒 none 默认永不过期
redis  雪崩 产生的主要原因是同一时刻大量的数据同时过期
        解决方法   在设置缓存的时间上加上随机数
key_prefix 设置缓存key的前缀
    存入redis数据库名的前缀 如果不加该参数默认数据库名为 flask_cache_view// 
'''
@main.route('/')
@cache.cached(timeout=20 +random.randint(10,60) ,key_prefix='view_index')
def index():
    return render_template('index.html',now=datetime.datetime.now())

'''
cached 不支持视图函数带参数
memoize 支持视图函数带参数
参数说明：
timeout
make_name 
'''
@main.route('/<int:id>/')
@cache.memoize(timeout=20)
def detail(id):
    return render_template('index.html',id=id,now=datetime.datetime.now())

@main.route('/temp/')
def temp_cache():
    return render_template('temp_cache.html',now=datetime.datetime.now())
