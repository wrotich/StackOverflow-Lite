import os
postgres_local_base = 'postgresql://postgres:@localhost/'
database_name = 'testdb'

class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_pin')
    DEBUG = False
  
    


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
  


class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
 

class ProductionConfig(BaseConfig):
    """Production configuration."""
    SECRET_KEY = 'my_pin'
    DEBUG = False
