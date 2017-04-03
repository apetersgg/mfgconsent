import unittest
from app.models import User

# import pydevd

class UserModelTestCase(unittest.TestCase):
        # pydevd.settrace('192.168.56.1', port=22, stdoutToServer=True, stderrToServer=True)
        def test_password_setter(self):
            u = User(password = 'cat')
            self.assertTrue(u.password_hash is not None)

        def test_no_password_getter(self):
            u = User(password='cat')
            with self.assertRaises(AttributeError):
                pass
                # u.password

        def test_password_verification(self):
            u = User(password='cat')
            self.assertTrue(u.verify_password('cat'))
            self.assertFalse(u.verify_password('dog'))

        def test_password_salts_are_random(self):
            u = User(password='cat')
            u2 = User(password='cat')
            self.assertTrue(u.password_hash != u2.password_hash)