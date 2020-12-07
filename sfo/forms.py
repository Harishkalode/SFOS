from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, \
    RadioField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from sfo.models import Admin, Student


class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = Admin.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exist in our system, please try another one')


class RegistrationForm2(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    mname = StringField('Middle Name', validators=[DataRequired(), Length(min=2, max=20)])
    lname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    institution_name = StringField('Institution Name', validators=[DataRequired()])
    institution_email = StringField("Institution Email", validators=[DataRequired()])
    phone_no = StringField('Phone No', validators=[DataRequired(), Length(min=10, max=10)])
    dob = StringField('Date Of Birth', validators=[DataRequired()])
    institution_address = StringField('Institution Address', validators=[DataRequired()])
    institution_website_link = StringField('Institution Website Link')
    linkedin_link = StringField('Linkedin Link')
    instagram_link = StringField('Instagram Link')
    facebook_link = StringField('Facebook Link')
    submit = SubmitField('Continue')

    def validate_phone_no(self, phone_no):
        admin = Admin.query.filter_by(phone_no=phone_no.data).first()
        if admin:
            raise ValidationError('We already have this phone number in our account, please try another one')

    def validate_institution_email(self, institution_email):
        admin = Admin.query.filter_by(institution_email=institution_email.data).first()
        if admin:
            raise ValidationError('We already have this email in our account, please try another one')


class AccountUpdateForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    status = StringField("Status", validators=[DataRequired()])
    fname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    mname = StringField('Middle Name', validators=[DataRequired(), Length(min=2, max=20)])
    lname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    dob = StringField('Date Of Birth', validators=[DataRequired()])
    institution_name = StringField('Institution Name', validators=[DataRequired()])
    institution_email = StringField("Institution Email", validators=[DataRequired()])
    phone_no = StringField('Phone No', validators=[DataRequired(), Length(min=10, max=10)])
    profile_img = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    institution_logo = FileField('Update Institution Logo', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    institution_address = StringField('Institution Address', validators=[DataRequired()])
    institution_website_link = StringField('Institution Website Link')
    linkedin_link = StringField('Linkedin Link')
    instagram_link = StringField('Instagram Link')
    facebook_link = StringField('Facebook Link')
    submit = SubmitField('Continue')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = Admin.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already exist in our system, please try another one')

    def validate_phone_no(self, phone_no):
        if phone_no.data != current_user.phone_no:
            admin = Admin.query.filter_by(phone_no=phone_no.data).first()
            if admin:
                raise ValidationError('We already have this phone number in our account, please try another one')

    def validate_institution_email(self, institution_email):
        if institution_email.data != current_user.institution_email:
            admin = Admin.query.filter_by(institution_email=institution_email.data).first()
            if admin:
                raise ValidationError('We already have this email in our account, please try another one')


class AddStudentForm(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    father_name = StringField('Father Name', validators=[DataRequired(), Length(min=2, max=20)])
    mother_name = StringField('Mother Name', validators=[DataRequired(), Length(min=2, max=20)])
    lname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired()])
    roll_no = StringField('Roll No.', validators=[DataRequired()])
    father_occupation = StringField('Father Occupation', validators=[DataRequired()])
    mother_occupation = StringField('Mother Occupation', validators=[DataRequired()])
    father_income = StringField('Father Income', validators=[DataRequired()])
    mother_income = StringField('Mother Income', validators=[DataRequired()])
    father_phone_no = StringField('Father Phone No', validators=[DataRequired(), Length(min=10, max=10)])
    mother_phone_no = StringField('Mother Phone No', validators=[DataRequired(), Length(min=10, max=10)])
    p_address = StringField('Postal Address', validators=[DataRequired()])
    l_address = StringField('Local Address', validators=[DataRequired()])
    phone_no = StringField('Phone No', validators=[DataRequired(), Length(min=10, max=10)])
    dob = StringField('Date of Birth', validators=[DataRequired()])
    religion = StringField('Religion', validators=[DataRequired()])
    caste = StringField('Caste', validators=[DataRequired()])
    gender = StringField('Gender', validators=[DataRequired()])
    blood_group = StringField('Blood Group', validators=[DataRequired()])
    profile_img = FileField('Student Profile', validators=[DataRequired(), FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Add Student')

    def validate_email(self, email):
        student = Student.query.filter_by(email=email.data).first()
        if student:
            raise ValidationError('Email already exist in our system, please try another one')

    def validate_phone_no(self, phone_no):
        student = Student.query.filter_by(phone_no=phone_no.data).first()
        if student:
            raise ValidationError('We already have this phone number in our account, please try another one')


class UpdateStudentForm(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    father_name = StringField('Father Name', validators=[DataRequired(), Length(min=2, max=20)])
    mother_name = StringField('Mother Name', validators=[DataRequired(), Length(min=2, max=20)])
    lname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired()])
    roll_no = StringField('Roll No.', validators=[DataRequired()])
    father_occupation = StringField('Father Occupation', validators=[DataRequired()])
    mother_occupation = StringField('Mother Occupation', validators=[DataRequired()])
    father_income = StringField('Father Income', validators=[DataRequired()])
    mother_income = StringField('Mother Income', validators=[DataRequired()])
    father_phone_no = StringField('Father Phone No', validators=[DataRequired(), Length(min=10, max=10)])
    mother_phone_no = StringField('Mother Phone No', validators=[DataRequired(), Length(min=10, max=10)])
    p_address = StringField('Postal Address', validators=[DataRequired()])
    l_address = StringField('Local Address', validators=[DataRequired()])
    phone_no = StringField('Phone No', validators=[DataRequired(), Length(min=10, max=10)])
    dob = StringField('Date of Birth', validators=[DataRequired()])
    religion = StringField('Religion', validators=[DataRequired()])
    caste = StringField('Caste', validators=[DataRequired()])
    gender = StringField('Gender', validators=[DataRequired()])
    blood_group = StringField('Blood Group', validators=[DataRequired()])
    profile_img = FileField('Student Profile', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Update Student')

    def validate_email(self, email):
        student = Student.query.filter_by(email=email.data).first()
        if email.data != student.email:
            if student:
                raise ValidationError('Email already exist in our system, please try another one')

    def validate_phone_no(self, phone_no):
        student = Student.query.filter_by(phone_no=phone_no.data).first()
        if phone_no.data != student.phone_no:
            if student:
                raise ValidationError('We already have this phone number in our account, please try another one')


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField('Log me in')


class AddSubjectForm(FlaskForm):
    subject = StringField("Subject", validators=[DataRequired()])
    standard = SelectField("Standard", choices=[('1st', '1st'),
                                                ('2nd', '2nd'), ('3rd', '3rd'), ('4th', '4th'), ('5th', '5th'),
                                                ('6th', '6th'),
                                                ('7th', '7th'), ('8th', '8th'), ('9th', '9th'), ('10th', '10th'),
                                                ('11th', '11th'), ('12th', '12th'), ('Poly 1st year', 'Poly 2nd year'),
                                                ('Poly 3rd year', 'Poly 3rd year'),
                                                ('Degree 1st year', 'Degree 1st year'),
                                                ('Degree 2nd year', 'Degree 2nd year'),
                                                ('Degree 3rd year', 'Degree 3rd year'),
                                                ('Degree 4th year', 'Degree 4th year'),
                                                ('Degree 5th year', 'Degree 5th year')],
                           validators=[DataRequired()])
    institute_subject = RadioField("Does this Subject Belongs to your Institute",
                                   choices=[('ON', 'ON'), ('YES', 'YES')], validators=[DataRequired()])
    submit = SubmitField('Add Subject')


class UpdateSubjectForm(FlaskForm):
    subject = StringField("Subject", validators=[DataRequired()])
    standard = SelectField("Standard", choices=[('1st', '1st'),
                                                ('2nd', '2nd'), ('3rd', '3rd'), ('4th', '4th'), ('5th', '5th'),
                                                ('6th', '6th'),
                                                ('7th', '7th'), ('8th', '8th'), ('9th', '9th'), ('10th', '10th'),
                                                ('11th', '11th'), ('12th', '12th'), ('Poly 1st year', 'Poly 2nd year'),
                                                ('Poly 3rd year', 'Poly 3rd year'),
                                                ('Degree 1st year', 'Degree 1st year'),
                                                ('Degree 2nd year', 'Degree 2nd year'),
                                                ('Degree 3rd year', 'Degree 3rd year'),
                                                ('Degree 4th year', 'Degree 4th year'),
                                                ('Degree 5th year', 'Degree 5th year')],
                           validators=[DataRequired()])
    institute_subject = RadioField("Does this Subject Belongs to your Institute",
                                   choices=[('ON', 'ON'), ('YES', 'YES')], validators=[DataRequired()])
    submit = SubmitField('Update Subject')


class AddExamForm(FlaskForm):
    subject = SelectField("Subject", choices=[], validators=[DataRequired()])
    marks_opt = StringField('Marks Obtain', validators=[DataRequired()])
    institution_name = StringField('Institution Name', validators=[DataRequired()])
    submit = SubmitField('Continue')


class RequestResetForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField('Request Password reset')

    def validate_email(self, email):
        admin = Admin.query.filter_by(email=email.data).first()
        if admin is None:
            raise ValidationError("Email dose not exist in our system")


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
