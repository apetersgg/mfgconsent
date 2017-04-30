import os

import pydevd

basedir = os.path.abspath(os.path.dirname(__file__))

# You can use .bashrc to set persistent environment variables
# Use export KEY=value on command line to set environ variable
# Use unset KEY on command line to unset an environ variable
# Use echo "$SECRET_KEY" to view the variable on the command line


class Config:
    def __init__(self):
        pass

    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'Password'
    SSL_DISABLE = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True

    MAIL_SERVER = 'smtp.sendgrid.net'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'transreductionist@gmail.com'
    MAIL_PASSWORD = 'xXsrCEsH2fHZ2'

    MFGCONSENT_MAIL_SUBJECT_PREFIX = '[Mfg Consent]'
    MFGCONSENT_MAIL_SENDER = 'transreductionist@gmail.com'
    MFGCONSENT_ADMIN = 'apeters'
    MFGCONSENT_POSTS_PER_PAGE = 25
    MFGCONSENT_FOLLOWERS_PER_PAGE = 25
    MFGCONSENT_COMMENTS_PER_PAGE = 25
    MFGCONSENT_SLOW_DB_QUERY_TIME=0.5

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.sendgrid.net'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'transreductionist@gmail.com'
    MAIL_PASSWORD = 'xXsrCEsH2fHZ2'
    SQLALCHEMY_DATABASE_URI = 'mysql://apeters:Password@192.168.75.1:3306/mfgconsent'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://apeters:Password@192.168.75.1:3306/mfgconsent'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://apeters:Password@192.168.75.1:3306/mfgconsent'

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)

            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()

        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.MFGCONSENT_MAIL_SENDER,
            toaddrs=[cls.MFGCONSENT_ADMIN],
            subject=cls.MFGCONSENT_MAIL_SUBJECT_PREFIX + ' Application Error',
            credentials=credentials,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


class HerokuConfig(ProductionConfig):
    SSL_DISABLE = bool(os.environ.get('SSL_DISABLE'))

    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # Handle proxy server headers
        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)

        # Log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)


class UnixConfig(ProductionConfig):
    @classmethod
    def init_app(app):
        ProductionConfig.init_app(app)

        # Log to syslog
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'heroku': HerokuConfig,
    'unix': UnixConfig,

    'default': DevelopmentConfig
}




