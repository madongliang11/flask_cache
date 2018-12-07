from flask import Blueprint, render_template
from flask import request

from apps.account.models import Image
from apps.ext import img_set, db, doc_set
from apps.upfile import helper

upload = Blueprint('upload',__name__,template_folder='templates')

'''
如何避免文件上传时候重名
对文件的名字重命名
对上传文件的目录尽量细分

'''

@upload.route('/upload/',methods=['get','post','put'])
def upload_image():
    if request.method == 'GET':
        return render_template('upload.html')
    else:
        # 通过files获取storate对象
        image_file = request.files['img']
        # 通过UploadSet对象
        # folder  设置文件上传的子文件夹
        # name 重命名文件名
        image_name = helper.get_file_name(image_file.filename)
        file_name = img_set.save(image_file,folder='user/1',name=image_name)
        # 生成访问文件的路径
        img_url = img_set.url(file_name)
        try:
            img = Image(path=img_url,type=1,uid=1)
            db.session.add(img)
            db.session.commit()
        except:
            db.session.rollback()
        return render_template('image.html',img_url=img_url)

@upload.route('/save/',methods=['get','post'])
def upload_files():
    if request.method == 'GET':
        return render_template('doc.html')
    else:
        file_str = request.files['doc']
        doc_name = doc_set.save(file_str)
        url = doc_set.url(doc_name)
        return '成功'


