import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # FIXME deepcode ignore HardcodedNonCryptoSecret: <please specify a reason of ignoring this>
    SECRET_KEY = ';kjasicl4tiwueliaulascruyalkr'  # TODO regenerate

    SERVER_NAME = "encs3340.unv.ibraheemalyan.dev"
    DOMAIN_NAME = "encs3340.unv.ibraheemalyan.dev"

    SSL_REDIRECT = True

    # ######## Cookies ########

    WTF_CSRF_ENABLED = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):

    SERVER_NAME = "dev-silal.com:8080"
    DOMAIN_NAME = "dev-silal.com"

    REMEMBER_COOKIE_SECURE = False

    REMEMBER_COOKIE_NAME = "remember"
    SESSION_COOKIE_NAME = "session"

    EMAIL_OTP_LIFE_IN_SECONDS = 300  # 5 minutes
    SMS_OTP_LIFE_IN_SECONDS = 60  # 1 minute

    DEBUG = True
    SSL_REDIRECT = False
    WTF_CSRF_ENABLED = False

    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # SQLALCHEMY_ECHO=True

    # SQLite config

    # SQLALCHEMY_DATABASE_URI = os.environ.get(
    #     "DEV_DATABASE_URL"
    # ) or "sqlite:///" + os.path.join(os.path.dirname(basedir), "data-dev.sqlite")

    # Postgresql config

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEV_DATABASE_URL"
    ) or "postgresql+psycopg2://silal_agent:PasSw0rd@127.0.0.1:5432/"

    # SQLALCHEMY_DATABASE_URI = os.environ.get("REMOTE_DEV_DATABASE_URL")

    @staticmethod
    def init_app(app):
        pass


class TestingConfig(DevelopmentConfig):
    '''  to be run for PyTest in Github Actions '''

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEV_DATABASE_URL"
    ) or "sqlite:///" + os.path.join(os.path.dirname(basedir), "data-dev.sqlite")

class RemoteDevelopmentConfig(DevelopmentConfig):

    SERVER_NAME = "dev.silal.app"
    DOMAIN_NAME = "dev.silal.app"

    SQLALCHEMY_DATABASE_URI = os.environ.get("REMOTE_DEV_DATABASE_URL")
    SSL_REDIRECT = False

    REDIRECT_URI = "https://www." + SERVER_NAME + "/auth/oauth2/google/callback"

    @classmethod
    def init_app(cls, app):

        DevelopmentConfig.init_app(app)

        # log to stderr
        import logging

        gunicorn_error_logger = logging.getLogger("gunicorn.error")
        app.logger.handlers.extend(gunicorn_error_logger.handlers)
        app.logger.setLevel(logging.DEBUG)

        app.logger.debug("RemoteDevelopmentConfig was loaded")


class AWSDevelopmentConfig(RemoteDevelopmentConfig):

    SERVER_NAME = "dev.aws.silal.app"
    DOMAIN_NAME = "dev.aws.silal.app"

    SQLALCHEMY_DATABASE_URI = os.environ.get("AWS_RDS_DATABASE_URL")
    SSL_REDIRECT = False

    #    TODO add aws links to google console
    REDIRECT_URI = "https://www." + SERVER_NAME + "/auth/oauth2/google/callback"


# TODO
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "data.sqlite")

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # email errors to the administrators
        import logging
        from logging.handlers import SMTPHandler

        credentials = None
        secure = None
        if getattr(cls, "MAIL_USERNAME", None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, "MAIL_USE_TLS", None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.FLASKY_MAIL_SENDER,
            toaddrs=[cls.FLASKY_ADMIN_EMAIL],
            subject=cls.FLASKY_MAIL_SUBJECT_PREFIX + " Application Error",
            credentials=credentials,
            secure=secure,
        )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


config_modes: dict[str, Config] = {
    "development": DevelopmentConfig,
    "remote_development": RemoteDevelopmentConfig,
    "aws_development": AWSDevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "raw": Config,
}
