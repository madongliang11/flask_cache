import datetime

from apps.ext import db

'''
1、在子表上键外键字段
2、创建关联关系
    老版本 只在主表中建立关联关系db.relationship（）通过backref参数建立相互关联
    新版本 主表和字表都要建立关联关系
'''
class User(db.Model):
    uid = db.Column(db.Integer,autoincrement=True,primary_key=True)
    username = db.Column(db.String(100),unique=True,index=True,nullable=False)
    image = db.relationship('Image',back_populates='user',uselist=False)

# dynamic 只能用于一对多，或者多对多的关系
class Image(db.Model):
    img_id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    path = db.Column(db.String(255),unique=True,default='')
    # 1表示用户头像  2表示商户头像
    type = db.Column(db.SmallInteger,nullable=False)
    create_date = db.Column(db.DateTime,default=datetime.datetime.now())
    # 外键字段(主表类名.字段)
    # 查询字段
    uid = db.Column(db.Integer,db.ForeignKey(User.uid),unique=True)
    user = db.relationship('User', back_populates='image',uselist=False)