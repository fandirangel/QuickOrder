import os

class Config:
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
         # Fallback local
        database_url = 'postgresql://postgres:Talon1528@localhost/Proyectocloud'
    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join('static','uploads')