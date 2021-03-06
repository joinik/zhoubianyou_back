class DefaultConfig:
    """默认配置"""
    # 数据库mysql配置
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@192.168.17.131:3306/suixinyou1"
    SQLALCHEMY_TRACK_MODIFICATIONS = False # 是否追踪数据变化
    SQLALCHEMY_ECHO = False # 是否打印底层执行的sql

    # redis配置
    REDIS_HOST = '192.168.17.131'  # ip
    REDIS_PORT = 6381  # 端口

    # JWT
    JWT_SECRET = 'YKrPUNI7eCrz6h6cgX0VFYVYNhzz9p+gqGxxAEAhXwo/MLRWKaPbAw=='  # 秘钥
    JWT_EXPIRE_DAYS = 14  # JWT过期时间
    JWT_EXPIRE_HOURS = 2  # token 过期时间

    # 七牛云
    QINIU_ACCESS_KEY = '4-vVQInCM2SjXzkeEeI5sFA1ExaCuY0rCxnAb2JB'
    QINIU_SECRET_KEY = '9QK46pawEesuxyIvn2wuo6G-X_oSMG6Cg5NQnekP'
    QINIU_BUCKET_NAME = 'suixinyou1'
    QINIU_DOMAIN = 'http://r7r21o73n.hn-bkt.clouddn.com/'


config_dict = {
    'dev': DefaultConfig
}


if __name__ == '__main__':
    import os, base64
    # 生成随机字符串, 可用于秘钥
    randowm_str = base64.b64encode(os.urandom(40)).decode()
    print(randowm_str)
    print(len(randowm_str))
    print(len('N1UzXOFKJRZk5cslhMDcbqHZ0lKvCAyL85fufewVmUF9bGPAlAXw9w=='))