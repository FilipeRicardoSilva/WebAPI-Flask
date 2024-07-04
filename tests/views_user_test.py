import unittest
from flask import session
from gamestory import app, db
from models import Usuarios
from flask_bcrypt import generate_password_hash

class TestAuth(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False 
        self.app = app.test_client()

        self.app_context = app.app_context()
        self.app_context.push()

        db.create_all()

        self.user = Usuarios(nome='Usuário de Teste', nickname='testuser',
                             senha=generate_password_hash('testpassword').decode('utf-8'))
        db.session.add(self.user)
        db.session.commit()

    def test_login_logout(self):
        rv = self.app.post('/autenticar', data=dict(
            nickname='testuser',
            senha='testpassword',
            proxima='/'
        ), follow_redirects=True)
        self.assertIn(b'logado com sucesso', rv.data)
        self.assertEqual(session['usuario_logado'], 'testuser')

        rv = self.app.get('/logout', follow_redirects=True)
        self.assertIn(b'Logout efetuado com sucesso', rv.data)
        self.assertIsNone(session.get('usuario_logado'))

    def tearDown(self):
        db.session.remove()
        db.drop_all()

        self.app_context.pop()

if __name__ == '__main__':
    unittest.main()
