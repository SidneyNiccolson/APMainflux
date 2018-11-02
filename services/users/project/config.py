import os


class BaseConfig:
    """Base configuration"""
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    VERIFY_HTTPS = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    BCRYPT_LOG_ROUNDS = 13
    TOKEN_EXPIRATION_DAYS = 30
    TOKEN_EXPIRATION_SECONDS = 0


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    MAINFLUX_ADDRESS = os.environ.get('MAINFLUX_BROKER_URL')
    VERIFY_HTTPS = False
    DEBUG_TB_ENABLED = True
    BCRYPT_LOG_ROUNDS = 4


class TestingConfig(BaseConfig):
    """Testing configuration"""
    TESTING = True
    VERIFY_HTTPS = os.environ.get('VERIFY_HTTPS')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')
    MAINFLUX_ADDRESS = os.environ.get('MAINFLUX_BROKER_URL')
    VERIFY_HTTPS = False
    BCRYPT_LOG_ROUNDS = 4
    TOKEN_EXPIRATION_DAYS = 0
    TOKEN_EXPIRATION_SECONDS = 3


class ProductionConfig(BaseConfig):
    """Production configuration"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    MAINFLUX_ADDRESS = os.environ.get('MAINFLUX_BROKER_URL')
    VERIFY_HTTPS = os.environ.get('VERIFY_HTTPS')
    VERIFY_HTTPS = True
