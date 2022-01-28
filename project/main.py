from models import Teacher, Student, Course, StudentCourse
from flask import request
from flask.helpers import make_response
from flask.json import jsonify
from sqlalchemy import insert
from sqlalchemy.orm import session, sessionmaker
from marshmallow import Schema
from app import app, db, bcrypt, teacher_auth, student_auth


@teacher_auth.verify_password
def verify_password(email, password):
    user = Teacher.query.filter(Teacher.TEmail == email).first()
    if user and bcrypt.check_password_hash(user.TPassword, password):
        return user
    return


@student_auth.verify_password
def verify_password_student(email, password):
    user = Student.query.filter(Student.SEmail == email).first()
    if user and bcrypt.check_password_hash(user.SPassword, password):
        return user
    return


@app.route('/')
def index():
    return "Main Page"


# Teacher
@app.route('/teacher', methods=['POST'])
def add_teacher():
    """
    Add a teacher
    """

    teacher_name_ = request.json['teacher_name_']
    teacher_surname_ = request.json['teacher_surname_']
    teacher_email_ = request.json['teacher_email_']
    teacher_password_ = request.json['teacher_password_']

    if not all([teacher_name_, teacher_surname_, teacher_email_, teacher_password_]):
        return make_response(jsonify({"400": "check and write correct info"}), 400)

    teacher_password_ = bcrypt.generate_password_hash(teacher_password_).decode('utf-8')

    obj = Teacher(teacher_name_, teacher_surname_, teacher_email_, teacher_password_)
    db.session.add(obj)
    db.session.commit()
    return make_response(jsonify({"200": "successful operation"}), 200)


@app.route('/teacher/<int:id_teacher>', methods=['GET'])
@teacher_auth.login_required
def teacher_courses(id_teacher):
    """
    Shows courses and applications of teacher with id = id_teacher
    """
    if teacher_auth.current_user().idTeacher != id_teacher:
        return make_response(jsonify({"400": "Log in with your ID!"}), 400)

    if not Teacher.query.filter(Teacher.idTeacher == id_teacher).first():
        return make_response(jsonify({"404": "Teacher with specified id not found"}), 404)
    else:
        courses = Course.query.filter(Course.Teacher_idTeacher == id_teacher).all()
        applications = StudentCourse.query.filter(StudentCourse.CSteachers_id == id_teacher)
        return make_response(jsonify({'Courses': [obj.serialize() for obj in courses],
                                      'Applications': [obj.view_application() for obj in applications]}), 200)


@app.route('/teacher/<int:id_teacher>/accept/<int:id_application>')
@teacher_auth.login_required
def accept_student(id_teacher, id_application):
    application = StudentCourse.query.filter(StudentCourse.idCourseStudent == id_application).first()

    if teacher_auth.current_user().idTeacher != id_teacher:
        return make_response(jsonify({"400": "Log in with your ID!"}), 400)

    if not Teacher.query.filter(Teacher.idTeacher == id_teacher).first():
        return make_response(jsonify({"404": "Teacher with specified id not found"}), 404)

    if not application:
        return make_response(jsonify({"404": "Application with specified id not found"}), 404)

    if application.CSteachers_id != id_teacher:
        return make_response(jsonify({"404": "This course belongs to the other teacher"}), 404)

    application.CSaccepted = True
    teacher_course = Course.query.filter(Course.idCourse == application.CScourse_id).first()
    teacher_course.Students_count += 1
    db.session.commit()
    return make_response(jsonify({"200": "successful operation"}), 200)


@app.route('/course/<int:id_teacher>', methods=['POST'])
@teacher_auth.login_required
def add_course(id_teacher):
    """
    Accepts JSON with keys:
        course_name_
        course_desc_
    """

    course_name_ = request.json['course_name_']
    course_desc_ = request.json['course_desc_']

    if teacher_auth.current_user().idTeacher != id_teacher:
        return make_response(jsonify({"400": "Log in with your ID!"}), 400)

    if not all([course_name_, course_desc_]):
        return make_response(jsonify({"400": "check and write correct info"}), 400)

    if not Teacher.query.filter(Teacher.idTeacher == id_teacher).first():
        return make_response(jsonify({"400": "Teacher with specified id not found"}), 404)

    course = Course(course_name_, course_desc_, id_teacher)
    db.session.add(course)
    db.session.commit()
    return make_response(jsonify({"200": "successful operation"}), 200)


@app.route('/teacher/<int:id_teacher>/course/<int:course_id>', methods=['PUT'])
@teacher_auth.login_required
def update_course(id_teacher, course_id):

    if teacher_auth.current_user().idTeacher != id_teacher:
        return make_response(jsonify({"400": "Log in with your ID!"}), 400)

    if not Teacher.query.filter(Teacher.idTeacher == id_teacher).first():
        return make_response(jsonify({"404": "Teacher with specified id not found"}), 404)

    if not Course.query.filter(Course.idCourse == course_id).first():
        return make_response(jsonify({"404": "Course with specified id not found"}), 404)

    course_name_ = request.json['course_name_']
    course_desc_ = request.json['course_desc_']

    course = Course.query.filter(Course.idCourse == course_id).first()
    course.Course_name = course_name_
    course.Course_desc = course_desc_
    db.session.commit()
    return make_response(jsonify({"200": "successful operation"}), 200)


@app.route('/teacher/<int:id_teacher>/course/<int:course_id>', methods=['DELETE'])
@teacher_auth.login_required
def delete_course(id_teacher, course_id):

    if teacher_auth.current_user().idTeacher != id_teacher:
        return make_response(jsonify({"400": "Log in with your ID!"}), 400)

    if not Teacher.query.filter(Teacher.idTeacher == id_teacher).first():
        return make_response(jsonify({"404": "Teacher with specified id not found"}), 404)

    if not Course.query.filter(Course.idCourse == course_id).first():
        return make_response(jsonify({"404": "Course with specified id not found"}), 404)

    if not Course.query.filter(Course.idCourse == course_id).first().Teacher_idTeacher != str(id_teacher):
        return make_response(jsonify({"400": "Course belongs to the other teacher"}), 400)

    course = Course.query.filter(Course.idCourse == course_id).first()
    db.session.delete(course)
    db.session.commit()
    return make_response(jsonify({"200": "successful operation"}), 200)


#Student
@app.route('/student', methods=['POST'])
def add_student():
    """
    Add a student
    """

    student_name_ = request.json['student_name_']
    student_surname_ = request.json['student_surname_']
    student_email_ = request.json['student_email_']
    student_password_ = request.json['student_password_']

    if not all([student_name_, student_surname_, student_email_, student_password_]):
        return make_response(jsonify({"400": "check and write correct info"}), 400)

    student_password_ = bcrypt.generate_password_hash(student_password_).decode('utf-8')

    obj = Student(student_name_, student_surname_, student_email_, student_password_)
    db.session.add(obj)
    db.session.commit()
    return make_response(jsonify(obj.serialize()), 200)


@app.route('/student/<int:student_id>', methods=['GET'])
@student_auth.login_required
def student_courses(student_id):

    if student_auth.current_user().idStudent != student_id:
        return make_response(jsonify({"400": "Log in with your ID!"}), 400)

    if not Student.query.filter(Student.idStudent == student_id).first():
        return make_response(jsonify({"404": "Student with specified id not found"}), 404)

    else:
        courses = StudentCourse.query.filter(StudentCourse.CSstudents_id == student_id and StudentCourse.CSaccepted)
        return make_response(jsonify([obj.serialize() for obj in courses]), 200)


@app.route('/student/<int:student_id>/application', methods=['POST'])
@student_auth.login_required
def enlist_for_courses(student_id):
    course_id = request.json['course_id']

    if student_auth.current_user().idStudent != student_id:
        return make_response(jsonify({"400": "Log in with your ID!"}), 400)

    if not Student.query.filter(Student.idStudent == student_id).first():
        return make_response(jsonify({"404": "Student with specified id not found"}), 404)

    if not Course.query.filter(Course.idCourse == course_id).first():
        return make_response(jsonify({"404": "Course with specified id not found"}), 404)

    if Course.query.filter(Course.idCourse == course_id).first().Students_count >= 5:
        return make_response(jsonify({"404": "Too many people registered for this course"}), 404)

    teacher_course = Course.query.filter(Course.idCourse == course_id).first()

    obj = StudentCourse(teacher_course.Teacher_idTeacher, student_id, course_id)
    db.session.add(obj)
    db.session.commit()
    return make_response(jsonify({"200": "successful operation"}), 200)


if __name__ == '__main__':
    app.run()
