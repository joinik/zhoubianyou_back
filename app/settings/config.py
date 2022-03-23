class DefaultConfig:
    """默认配置"""
    # 数据库mysql配置
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@172.26.243.224:3306/zhoubianyou"
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 是否追踪数据变化
    SQLALCHEMY_ECHO = False  # 是否打印底层执行的sql

    # redis配置
    REDIS_HOST = '172.26.243.224'  # ip
    REDIS_PORT = 6381
    # JWT
    JWT_SECRET = 'YKrPUNI7eCrz6h6cgX0VFYVYNhzz9p+gqGxxAEAhXwo/MLRWKaPbAw=='  # 秘钥
    JWT_EXPIRE_DAYS = 14  # JWT过期时间
    JWT_EXPIRE_HOURS = 2  # token 过期时间

    # 七牛云
    QINIU_ACCESS_KEY = '4-vVQInCM2SjXzkeEeI5sFA1ExaCuY0rCxnAb2JB'
    QINIU_SECRET_KEY = '9QK46pawEesuxyIvn2wuo6G-X_oSMG6Cg5NQnekP'
    QINIU_BUCKET_NAME = 'zhoubianyou'
    QINIU_DOMAIN = 'http://r94faay5k.hn-bkt.clouddn.com/'


config_dict = {

    'dev': DefaultConfig
}

# if __name__ == '__main__':
# import os, base64
# # 生成随机字符串, 可用于秘钥
# randowm_str = base64.b64encode(os.urandom(40)).decode()
# print(randowm_str)
