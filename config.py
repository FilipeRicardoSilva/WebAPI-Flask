import os

SECRET_KEY = 'auth'

SQLALCHEMY_DATABASE_URI = \
    'mysql+mysqlconnector://root:bp1234@localhost:3307/gamestory'

UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'