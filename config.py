class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = '\xec\xe0\xa7\x99\xba_^iM{:\xc7\xd55\xc5Y\x06\xf1\x1c\t"i\xf6\xa5'


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


