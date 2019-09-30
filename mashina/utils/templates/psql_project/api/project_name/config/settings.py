import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = False
TESTING_MODE = os.getenv('TESTING_MODE', False)
ALEMBIC_CFG_PATH = os.path.join(BASE_DIR, 'alembic.ini')

MIDDLEWARE = [
    'mashina.middlewares.cors.CORSComponent',
    'mashina.middlewares.initializer.InitializerMiddleware',
    'mashina.middlewares.sqlalchemy.SQLAlchemySessionMiddleware',
    'mashina.middlewares.json_translator.JSONTranslatorMiddleware',
]

APPS = [
]

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:@db:5432/postgres')
