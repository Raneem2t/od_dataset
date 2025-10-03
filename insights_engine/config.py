"""
Configuration settings for the Insights Engine application
"""

import os
from datetime import timedelta


class Config:
    """Base configuration class."""
    
    # Basic Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'insights-engine-secret-key-2024'
    
    # Database configuration (if needed in future)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # API Configuration
    API_VERSION = '1.0.0'
    API_TITLE = 'Insights Engine API'
    API_DESCRIPTION = 'AI-Powered Government Data Intelligence Platform'
    
    # CORS Configuration
    CORS_ORIGINS = ['http://localhost:3000', 'http://localhost:8000', 'http://127.0.0.1:5000']
    
    # Logging Configuration
    LOG_LEVEL = 'INFO'
    LOG_FORMAT = '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    
    # Expert System Configuration
    MAX_EXPERTS_PER_DATASET = 5
    MIN_STRATEGIC_ALIGNMENT_SCORE = 0.3
    DEFAULT_USE_CASE_PRIORITY = 'medium'
    
    # Context Engine Configuration
    MAX_EXTRACTED_KEYWORDS = 10
    MIN_CONTENT_RICHNESS_THRESHOLD = 0.2
    CONFIDENCE_SCORE_THRESHOLD = 0.5
    
    # Publishing System Configuration
    MAX_RECOMMENDATIONS_PER_REQUEST = 20
    DEFAULT_PUBLISHING_CAPACITY = 2  # datasets per quarter
    STRATEGIC_SCORE_THRESHOLD = 0.6
    
    # Data Loader Configuration
    DATA_DIR = 'data'
    LOGS_DIR = 'logs'
    CACHE_TIMEOUT = timedelta(hours=24)
    
    # Rate Limiting (if implementing)
    RATELIMIT_STORAGE_URL = 'memory://'
    RATELIMIT_DEFAULT = '100 per hour'
    
    # File Upload Configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'json', 'csv', 'txt'}
    
    # External API Configuration
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    OPENAI_MODEL = 'gpt-3.5-turbo'
    OPENAI_MAX_TOKENS = 1500
    
    # Cache Configuration
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 3600  # 1 hour
    
    @staticmethod
    def init_app(app):
        """Initialize application with configuration."""
        pass


class DevelopmentConfig(Config):
    """Development configuration."""
    
    DEBUG = True
    TESTING = False
    
    # More verbose logging in development
    LOG_LEVEL = 'DEBUG'
    
    # Allow all origins in development
    CORS_ORIGINS = ['*']
    
    # Disable some security features for development
    WTF_CSRF_ENABLED = False
    
    # Use simpler cache in development
    CACHE_TYPE = 'NullCache'
    
    @staticmethod
    def init_app(app):
        """Initialize development-specific settings."""
        app.logger.info('Starting in DEVELOPMENT mode')


class ProductionConfig(Config):
    """Production configuration."""
    
    DEBUG = False
    TESTING = False
    
    # Enhanced security in production
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Stricter CORS in production
    CORS_ORIGINS = [
        'https://your-domain.gov.sa',
        'https://insights.your-domain.gov.sa'
    ]
    
    # Production logging
    LOG_LEVEL = 'WARNING'
    
    # Redis cache in production
    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
    
    # Database URL for production
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
    @staticmethod
    def init_app(app):
        """Initialize production-specific settings."""
        import logging
        from logging.handlers import RotatingFileHandler
        
        # Setup rotating file handler
        file_handler = RotatingFileHandler(
            'logs/insights_engine.log',
            maxBytes=10240000,  # 10MB
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(Config.LOG_FORMAT))
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)
        
        app.logger.info('Starting in PRODUCTION mode')


class TestingConfig(Config):
    """Testing configuration."""
    
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    
    # Use in-memory database for testing
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    # Disable cache during testing
    CACHE_TYPE = 'NullCache'
    
    # Fast testing configurations
    MIN_STRATEGIC_ALIGNMENT_SCORE = 0.1
    CONFIDENCE_SCORE_THRESHOLD = 0.1
    
    @staticmethod
    def init_app(app):
        """Initialize testing-specific settings."""
        app.logger.info('Starting in TESTING mode')


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


# Expert System Configuration
EXPERT_CONFIGURATIONS = {
    'energy_efficiency': {
        'name': 'Energy Efficiency Expert',
        'domain': 'Energy & Sustainability',
        'min_keyword_matches': 2,
        'strategic_weight': 0.8,
        'enabled': True
    },
    'transportation': {
        'name': 'Transportation Expert',
        'domain': 'Transportation & Mobility',
        'min_keyword_matches': 2,
        'strategic_weight': 0.7,
        'enabled': True
    },
    'healthcare': {
        'name': 'Healthcare Expert',
        'domain': 'Healthcare & Social Services',
        'min_keyword_matches': 2,
        'strategic_weight': 0.9,
        'enabled': False  # Example: disabled expert
    }
}


# Domain Keyword Mappings (fallback if data files not available)
FALLBACK_DOMAIN_KEYWORDS = {
    'energy': [
        'energy', 'renewable', 'solar', 'wind', 'hydroelectric', 'nuclear',
        'electricity', 'power', 'grid', 'consumption', 'efficiency', 'carbon',
        'fuel', 'oil', 'gas', 'coal', 'biomass', 'geothermal', 'sustainability'
    ],
    'transportation': [
        'transport', 'transportation', 'traffic', 'vehicle', 'car', 'truck',
        'bus', 'metro', 'train', 'railway', 'road', 'highway', 'mobility',
        'logistics', 'freight', 'cargo', 'shipping', 'delivery', 'transit'
    ],
    'healthcare': [
        'health', 'healthcare', 'medical', 'hospital', 'patient', 'disease',
        'treatment', 'medicine', 'clinical', 'wellness', 'epidemiology',
        'pharmacy', 'surgery', 'diagnosis', 'therapy', 'prevention'
    ],
    'education': [
        'education', 'school', 'university', 'student', 'teacher', 'learning',
        'curriculum', 'academic', 'training', 'knowledge', 'skill', 'literacy',
        'research', 'scholarship', 'degree', 'certification'
    ],
    'environment': [
        'environment', 'environmental', 'climate', 'weather', 'pollution',
        'ecosystem', 'biodiversity', 'conservation', 'green', 'clean',
        'air quality', 'water quality', 'waste', 'recycling'
    ]
}


# Strategic Alignment Keywords
STRATEGIC_KEYWORDS = [
    'vision 2030', 'national transformation', 'digital transformation',
    'smart city', 'innovation', 'sustainability', 'diversification',
    'renewable energy', 'efficiency', 'transparency', 'governance',
    'public service', 'economic growth', 'social development',
    'infrastructure', 'technology', 'artificial intelligence',
    'automation', 'green initiative', 'carbon neutral', 'climate change',
    'neom', 'red sea project', 'quality of life', 'entertainment',
    'tourism', 'privatization', 'sme development'
]


# Use Case Templates
USE_CASE_TEMPLATE = {
    "title": "",
    "objective": "",
    "implementation": "",
    "strategic_alignment": [],
    "impact_areas": [],
    "priority": "medium",
    "timeline": "",
    "resources_required": [],
    "success_metrics": [],
    "generated_by": {
        "expert_name": "",
        "expert_domain": "",
        "generation_timestamp": ""
    }
}


# API Response Templates
API_RESPONSE_TEMPLATES = {
    "success": {
        "success": True,
        "data": {},
        "timestamp": "",
        "version": Config.API_VERSION
    },
    "error": {
        "success": False,
        "error": "",
        "details": "",
        "timestamp": "",
        "version": Config.API_VERSION
    }
}