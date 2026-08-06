import os

from dotenv import load_dotenv


load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")
    WTF_CSRF_TIME_LIMIT = 3600
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", "587"))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "true").lower() == "true"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", MAIL_USERNAME)
    MAIL_RECIPIENT = os.getenv("MAIL_RECIPIENT", "popoolaisaiah2003@gmail.com")
    MAIL_TIMEOUT = int(os.getenv("MAIL_TIMEOUT", "10"))


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

    @classmethod
    def init_app(cls, app):
        if cls.SECRET_KEY == "dev-only-change-me":
            raise RuntimeError("Set a secure SECRET_KEY in the production environment.")
        if not cls.MAIL_USERNAME or not cls.MAIL_PASSWORD:
            raise RuntimeError("Set MAIL_USERNAME and MAIL_PASSWORD in the production environment.")


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}