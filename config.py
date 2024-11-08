import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))
class Config:
    # 기본 설정
    SECRET_KEY = os.environ.get('SECRET_KEY') 
    
    # 데이터베이스 설정
    SQLALCHEMY_DATABASE_URI = 'sqlite:////home/turboguy36/ChristmasCard/app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
   
    # 파일 업로드 설정
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max-limit
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # 세션 설정
    PERMANENT_SESSION_LIFETIME = timedelta(days=31)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    
    # 캐시 설정
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 300
    
    DEBUG = True
    
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True  # SQL 쿼리 로깅 활성화

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_ECHO = False

# 환경 변수에 따른 설정 선택
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}