import os

class Config:
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB limit
