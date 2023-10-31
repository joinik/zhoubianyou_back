class DefaultConfig:
    """默认配置"""
    # 数据库mysql配置

    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@192.168.0.225:3306/zhoubianyou"
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 是否追踪数据变化
    SQLALCHEMY_ECHO = False  # 是否打印底层执行的sql

    # redis配置
    REDIS_HOST = '192.168.0.225'  # ip
    REDIS_PORT = 7000
    # JWT
    JWT_SECRET = 'YKrPUNI7eCrz6h6cgX0VFYVYNhzz9p+gqGxxAEAhXwo/MLRWKaPbAw=='  # 秘钥
    JWT_EXPIRE_DAYS = 14  # JWT过期时间
    JWT_EXPIRE_HOURS = 2  # token 过期时间

    # 七牛云
    QINIU_ACCESS_KEY = ''
    QINIU_SECRET_KEY = ''

    QINIU_BUCKET_NAME = 'suixinyou3'
    QINIU_DOMAIN = 'http://ra1r2qeyc.hd-bkt.clouddn.com/'


config_dict = {
    'dev': DefaultConfig
}



