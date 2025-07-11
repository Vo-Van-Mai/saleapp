import unittest
from app import dao, app

class TestLogin(unittest.TestCase):
    def test_success(self):
        with app.app_context():  # 👉 kích hoạt app context để truy vấn CSDL
            user = dao.auth_user("admin", "123456")
            self.assertIsNotNone(user)
            self.assertEqual(user.username, "user")

if __name__ == '__main__':
    unittest.main()
