from .development import DevelopmentConfig
from .production import ProductionConfig
from .testing import TestingConfig

config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
