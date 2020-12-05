from sfo import db, login_manager, app
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(120), nullable=True)
    mname = db.Column(db.String(120), nullable=True)
    lname = db.Column(db.String(120), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    status = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    institution_name = db.Column(db.String(220), nullable=True)
    institution_email = db.Column(db.String(220), unique=True, nullable=True)
    phone_no = db.Column(db.String(20), unique=True, nullable=True)
    dob = db.Column(db.String(20), nullable=True)
    profile_img = db.Column(db.String(220), nullable=False, default="default.jpg")
    institution_logo = db.Column(db.String(220), nullable=False, default="default.jpg")
    institution_address = db.Column(db.String(1220), nullable=True)
    institution_website_link = db.Column(db.String(2200), nullable=True)
    linkedin_link = db.Column(db.String(220), nullable=True)
    instagram_link = db.Column(db.String(220), nullable=True)
    facebook_link = db.Column(db.String(220), nullable=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    students = db.relationship('Student', backref='admin', lazy=True)
    subjects = db.relationship('Subject', backref='admin', lazy=True)
    history = db.relationship('History', backref='admin', lazy=True)

    def get_reset_token(self, expire_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expire_sec)
        return s.dumps({'admin_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            admin_id = s.loads(token)['admin_id']
        except:
            return None
        return Admin.query.get(admin_id)

    def __repr__(self):
        return f"User('{self.email}','{self.status}','{self.fname}','{self.lname}'," \
               f"'{self.college_name}','{self.dept_email}')"


class Student(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(120), nullable=True)
    father_name = db.Column(db.String(120), nullable=True)
    mother_name = db.Column(db.String(120), nullable=True)
    lname = db.Column(db.String(120), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    roll_no = db.Column(db.String(20), nullable=False)
    father_occupation = db.Column(db.String(120), nullable=True)
    father_income = db.Column(db.String(120), nullable=True)
    father_phone_no = db.Column(db.String(120), nullable=True)
    mother_occupation = db.Column(db.String(120), nullable=True)
    mother_income = db.Column(db.String(120), nullable=True)
    mother_phone_no = db.Column(db.String(120), nullable=True)
    p_address = db.Column(db.String(120), nullable=True)
    l_address = db.Column(db.String(120), nullable=True)
    phone_no = db.Column(db.String(20), unique=True, nullable=True)
    dob = db.Column(db.String(20), nullable=True)
    religion = db.Column(db.String(20), nullable=True)
    caste = db.Column(db.String(20), nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    standard = db.Column(db.String(20), nullable=True)
    blood_group = db.Column(db.String(20), nullable=True)
    profile_img = db.Column(db.String(220), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)
    exams = db.relationship('Exam', backref='student', lazy=True)

    def __repr__(self):
        return f"Student('{self.email}','{self.fname}','{self.lname}','{self.roll_no}','{self.admin_id}')"


subject_exam = db.Table("subject_exam",
                        db.Column('subject_id', db.Integer, db.ForeignKey('subject.id'), primary_key=True),
                        db.Column('exam_id', db.Integer, db.ForeignKey('exam.id'), primary_key=True)
                        )


class Subject(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(120), nullable=True)
    standard = db.Column(db.String(120), nullable=True)
    min_marks = db.Column(db.String(120), nullable=True)
    max_marks = db.Column(db.String(120), nullable=True)
    institute_subject = db.Column(db.String(4), nullable=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)
    exams = db.relationship('Exam', backref='subject', lazy=True)

    def __repr__(self):
        return f"Subject('{self.subject}','{self.standard}','{self.admin_id}')"


class History(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name_of_module = db.Column(db.String(120), nullable=False)
    activity = db.Column(db.String(120), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)

    def __repr__(self):
        return f"History('{self.name_of_module}','{self.activity}','{self.date_created}','{self.admin_id}')"


class Exam(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    exam_name = db.Column(db.String(120), nullable=True)
    marks_opt = db.Column(db.String(120), nullable=True)
    standard = db.Column(db.String(120), nullable=True)
    institution_name = db.Column(db.String(220), nullable=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)

    subjects = db.relationship('Subject', secondary=subject_exam)
