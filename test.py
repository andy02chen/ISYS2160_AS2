from localShop import db, app
from hashing import *
import unittest

class TestReg(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.app_context().push()
        db.drop_all()
        db.create_all()
        # Adding admin user for testing (admin users will be added before website is loaded)
        admin_add = User(username = "admin", email = "admin", password = password_sh("admin"), isAdmin = True,
            firstName = "admin", lastName = "admin", phone = "admin", address = "admin")
        db.session.add(admin_add)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_registration(self):
        registration('user','pass','pass', 'email','first','last', 'phone','address')
        self.assertEqual(User.query.count(), 2)

    def test_registration_fail_username_dupe(self):
        registration('user','pass','pass', 'email','first','last', 'phone','address')
        self.assertEqual(registration('user','pass','pass', 'email2','first','last', 'phone','address'), 1)
        self.assertEqual(User.query.count(), 2)

    def test_registration_fail_email_dupe(self):
        registration('user','pass','pass', 'email','first','last', 'phone','address')
        self.assertEqual(registration('user1','pass','pass', 'email','first','last', 'phone','address'), 2)
        self.assertEqual(User.query.count(), 2)

    def test_login(self):
        registration('user', 'user', 'user', 'user','user','user','user','user')
        self.assertTrue(checking_login('user','user'))

    def test_login_fail(self):
        registration('user', 'user', 'user', 'user','user','user','user','user')
        self.assertEqual(checking_login('user','a'), 'password_err')

    def test_login_admin(self):
        self.assertEqual(checking_login('admin', 'admin'), "admin")

    def test_login_admin_fail(self):
        registration('user', 'user', 'user', 'user','user','user','user','user')
        self.assertTrue(checking_login('user', 'user'))
    
    def test_login_admin_invalid_user(self):
        self.assertEqual(checking_login('not registered', 'not registered'),'username_err')

if __name__ == '__main__':
    unittest.main()