from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
from app import db

Base = declarative_base()
metadata = Base.metadata


class Teacher(db.Model):
    __tablename__ = 'teacher'

    idTeacher = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TName = db.Column(db.String(45))
    TSurname = db.Column(db.String(45))
    TEmail = db.Column(db.String(45))
    TPassword = db.Column(db.String(200))

    def __init__(self, name, surname, email, password):
        self.TName = name
        self.TSurname = surname
        self.TEmail = email
        self.TPassword = password

    def __repr__(self):
        return f"<Teacher (ID='{self.idTeacher}',Name='{self.TName}', Surname='{self.TSurname}'," \
               f" Email='{self.TEmail}',Password='{self.TPassword}')>"

    def serialize(self):
        return {
            'idTeacher': self.idTeacher,
            'TName': self.TName,
            'TSurname': self.TSurname,
            'TEmail': self.TEmail,
            'TPassword': self.TPassword
        }


class Student(db.Model):
    __tablename__ = 'student'

    idStudent = db.Column(db.Integer, primary_key=True, autoincrement=True)
    SName = db.Column(db.String(45))
    SSurname = db.Column(db.String(45))
    SEmail = db.Column(db.String(45))
    SPassword = db.Column(db.String(200))

    def __init__(self, name, surname, email, password):
        self.SName = name
        self.SSurname = surname
        self.SEmail = email
        self.SPassword = password

    def __repr__(self):
        return f"<Student (ID='{self.idStudent}',Name='{self.SName}', Surname='{self.SSurname}'," \
               f" Email='{self.SEmail}',Password='{self.SPassword}')>"

    def serialize(self):
        return {
            'idStudent': self.idStudent,
            'SName': self.SName,
            'SSurname': self.SSurname,
            'SEmail': self.SEmail,
            'SPassword': self.SPassword
        }


class Course(db.Model):
    __tablename__ = 'course'

    idCourse = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Course_name = db.Column(db.String(45))
    Course_desc = db.Column(db.Text)
    Teacher_idTeacher = db.Column(db.Integer, db.ForeignKey('teacher.idTeacher'))
    Students_count = db.Column(db.Integer)

    def __init__(self, course_name, course_desc, teacher_id):
        self.Course_name = course_name
        self.Course_desc = course_desc
        self.Teacher_idTeacher = teacher_id
        self.Students_count = 0

    def __repr__(self):
        return f"<TeacherCourse (ID='{self.idCourse}',Name='{self. Course_name}', Description='{self.Course_desc}'," \
               f" Teacher='{self.Teacher_idTeacher}', Students='{self.Students_count}')>"

    def serialize(self):
        return {
            'idCourse': self.idCourse,
            'Course_name': self.Course_name,
            'Course_desc': self.Course_desc,
            'Teacher_idTeacher': self.Teacher_idTeacher,
            'Students_count': self.Students_count
        }


class StudentCourse(db.Model):
    __tablename__ = 'student_course'

    idCourseStudent = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CSteachers_id = db.Column(db.Integer, db.ForeignKey('teacher.idTeacher'))
    CSstudents_id = db.Column(db.Integer, db.ForeignKey('student.idStudent'))
    CSaccepted = db.Column(db.Boolean)
    CScourse_id = db.Column(db.Integer, db.ForeignKey('course.idCourse'))

    def __init__(self, teacher_id, student_id, course_id):
        self.CSteachers_id = teacher_id
        self.CSstudents_id = student_id
        self.CSaccepted = False
        self.CScourse_id = course_id

    def __repr__(self):
        return f"<StudentCourse (ID='{self.idCourseStudent}',Teacher='{self.CSteachers_id}', Student='{self.CSstudents}'," \
               f" Accepted='{self.CSaccepted}', Course='{self.CScourse_id}')>"

    def serialize(self):
        return {
            'idCourseStudent': self.idCourseStudent,
            'CSteachers_id': self.CSteachers_id,
            'CSstudents_id': self.CSstudents_id,
            'CSaccepted': self.CSaccepted,
            'CScourse_id': self.CScourse_id
        }

    def view_application(self):
        return {
            'idApplication': self.idCourseStudent,
            'idStudent': self.CSstudents_id,
            'idCourse': self.CScourse_id
        }

