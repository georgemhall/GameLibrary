# config.py

class Config(object):
	"""
	Section for common configurations spanning multiple environments
	"""

class DevConfig(Config):
	"""
	Section for development environment configuration
	"""
	DEBUG = True
	SQLALCHEMY_ECHO = True
	
class ProdConfig(Config):
	"""
	Section for production environment configuration
	"""
	DEBUG = False
	
app_config = {
	'development': DevConfig,
	'production': ProdConfig
}
