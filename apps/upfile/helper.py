
'''
对文件上传的名字重命名
'''
import datetime
import random

IMG_PREFIX_NAME = 'IMG'
def get_file_name(file_name:str):
    # 获取文件的后缀名
    suffix_name ='.' +  file_name.split('.')[-1]
    # 时间 + 随机数
    new_name = IMG_PREFIX_NAME + (datetime.datetime.now().strftime('%Y%m%d%H%M%S'))\
        + (str(random.randint(10000,99999)))
    return new_name + suffix_name

