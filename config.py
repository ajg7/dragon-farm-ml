"""
Configuration settings for Dragon Farm ML Service
"""

import os
from typing import Dict, Any

class Config:
    """Base configuration class."""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dragon-farm-ml-secret-key-2024'
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    
    # CORS settings for .NET backend communication
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5000,http://localhost:7000').split(',')
    
    # Logging settings
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Breeding engine settings
    BREEDING_ENGINE_CONFIG = {
        'enable_mutations': os.environ.get('ENABLE_MUTATIONS', 'true').lower() == 'true',
        'mutation_rate': float(os.environ.get('MUTATION_RATE', '0.05')),  # 5% mutation rate
        'min_breeding_success_rate': float(os.environ.get('MIN_BREEDING_SUCCESS_RATE', '10.0')),
        'max_breeding_success_rate': float(os.environ.get('MAX_BREEDING_SUCCESS_RATE', '95.0')),
        'enable_inbreeding_penalties': os.environ.get('ENABLE_INBREEDING_PENALTIES', 'true').lower() == 'true'
    }
    
    # .NET Backend communication settings
    DOTNET_BACKEND_CONFIG = {
        'base_url': os.environ.get('DOTNET_BACKEND_URL', 'http://localhost:7000'),
        'api_key': os.environ.get('DOTNET_API_KEY', ''),
        'timeout': int(os.environ.get('BACKEND_TIMEOUT', '30')),  # seconds
        'retry_attempts': int(os.environ.get('RETRY_ATTEMPTS', '3'))
    }
    
    # Database settings (if needed for future expansion)
    DATABASE_CONFIG = {
        'url': os.environ.get('DATABASE_URL', 'sqlite:///dragon_farm_ml.db'),
        'echo': os.environ.get('DATABASE_ECHO', 'false').lower() == 'true'
    }
    
    # Model settings
    MODEL_CONFIG = {
        'tensorflow_log_level': os.environ.get('TF_CPP_MIN_LOG_LEVEL', '2'),
        'enable_gpu': os.environ.get('ENABLE_GPU', 'false').lower() == 'true',
        'model_cache_dir': os.environ.get('MODEL_CACHE_DIR', './models/cache')
    }

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    LOG_LEVEL = 'WARNING'

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

# Configuration mapping
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config(config_name: str = None) -> Config:
    """
    Get configuration class based on environment.
    
    Args:
        config_name: Name of configuration to use
        
    Returns:
        Configuration class instance
    """
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    return config_map.get(config_name, DevelopmentConfig)()
