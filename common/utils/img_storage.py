from qiniu import Auth, put_data, etag
from flask import current_app



def upload_file(data):
    """
    上传文件到七牛云
    :param data: 要上传的二进制数据
    :return: 文件的名称
    """

    # 需要填写你的 Access Key 和 Secret Key
    access_key = current_app.config['QINIU_ACCESS_KEY']
    secret_key = current_app.config['QINIU_SECRET_KEY']

    # 构建鉴权对象
    q = Auth(access_key, secret_key)

    # 要上传的空间
    bucket_name = current_app.config['QINIU_BUCKET_NAME']

    # 上传后保存的文件名
    key = None  # 如果设置key=None, 则七牛云会自动生成名称(该名称会通过文件的哈希值生成, 不同文件的哈希值不同, 文件名不会出现冲突)
    # 哈希函数: 可以将任意长度的内容转为定长内容, 而且相同内容的哈希值一样, 不同内容的哈希值不同

    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)

    ret, info = put_data(token, key, data)
    if info.status_code == 200:  # 上传成功
        return current_app.config['QINIU_DOMAIN'] + ret.get('key')  # 获取并返回文件URL
    else:
        print("上传失败 。。。。")
        print(info.status_code)
        print(info.error)
        raise Exception(info.error)


if __name__ == '__main__':

    with open('../../123.png', 'rb') as f:
        data = f.read()  # 模拟前端上传的二进制数据
        file_url = upload_file(data)
        print(file_url)