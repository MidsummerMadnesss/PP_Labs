from flask_testing import TestCase
import unittest
from app import app, db
from models import Teacher, Student, Course, StudentCourse


class TestApp(TestCase):
    SQLALCHEMY_DATABASE_URI = r'sqlite:///D:\comp\db\testingdb.db'
    TESTING = True

    def create_app(self):
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_teacher_create(self):
        data = {'teacher_name_': 'One',
                'teacher_surname_': 'Two',
                'teacher_email_': 'example@gmail.com',
                'teacher_password_': '0000'}

        teacher = Teacher('One', 'Two', 'example@gmail.com', '0000')

        response = self.client.post('/teacher', json=data)

        self.assertEqual(response.json, {"200": "successful operation"})




if __name__ == '__main__':
    unittest.main()
