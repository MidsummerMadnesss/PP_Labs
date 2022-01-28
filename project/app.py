from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_httpauth import HTTPBasicAuth
from config import Configuration


app = Flask(__name__)
app.config.from_object(Configuration)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
teacher_auth = HTTPBasicAuth()
student_auth = HTTPBasicAuth()

import main

import main




# class TeachersSchema:
#     pass
#
#
# class StudentsSchema:
#     pass
#
#
# class CourseSchema:
#     pass
#
#
# class StudentCourseSchema:
#     pass
#
#
#
# teacher_schema = TeachersSchema()
# teachers_schema = TeachersSchema(many=True)
# student_schema = StudentSchema()
# students_schema = StudentSchema(many=True)
# student_email = ''
# teacher_email = ''
# course_schema = CourseSchema()
# courses_schema = CourseSchema(many=True)
# studentcourse_schema = StudentCourseSchema()
# studentcourses_schema = StudentCourseSchema(many=True)





# alembic revision --autogenerate -m "initial"
# alembic upgrade head
