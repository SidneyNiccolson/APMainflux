import os


class BaseConfig:
    """Base configuration"""
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'my_precious'
    VERIFY_HTTPS = True


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    MAINFLUX_ADDRESS = os.environ.get('MAINFLUX_BROKER_URL')
    VERIFY_HTTPS = False


class TestingConfig(BaseConfig):
    """Testing configuration"""
    TESTING = True
    VERIFY_HTTPS = os.environ.get('VERIFY_HTTPS')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')
    MAINFLUX_ADDRESS = os.environ.get('MAINFLUX_BROKER_URL')
    VERIFY_HTTPS = False


class ProductionConfig(BaseConfig):
    """Production configuration"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    MAINFLUX_ADDRESS = os.environ.get('MAINFLUX_BROKER_URL')
    VERIFY_HTTPS = os.environ.get('VERIFY_HTTPS')
    VERIFY_HTTPS = True
