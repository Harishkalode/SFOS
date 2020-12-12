from flask import render_template, url_for, flash, redirect, request
from sfo import app, db
from sfo.forms import AddStudentForm, UpdateStudentForm, AddExamForm, PromoteStudent
from sfo.models import Admin, Student, History, Subject, Exam
from flask_login import current_user, login_required
from sfo.routes import save_picture
from sfo.exam_routes import exam_view


@app.route("/add-student/new", methods=['GET', 'POST'])
@login_required
def add_student():
    form = AddStudentForm()
    page = request.args.get('page', 1, type=int)
    admin = Admin.query.filter_by(id=current_user.id).first_or_404()
    historys = History.query.filter_by(admin=admin).order_by(History.date_created.desc()).paginate(page=page,
                                                                                                   per_page=5)
    if form.validate_on_submit():
        if form.profile_img.data:
            picture_file1 = save_picture(form.profile_img.data)
            img = picture_file1
            student = Student(fname=form.fname.data,
                              father_name=form.father_name.data,
                              mother_name=form.mother_name.data,
                              lname=form.lname.data,
                              email=form.email.data,
                              roll_no=form.roll_no.data,
                              father_occupation=form.father_occupation.data,
                              father_income=form.father_income.data,
                              father_phone_no=form.father_phone_no.data,
                              mother_occupation=form.mother_occupation.data,
                              mother_income=form.mother_income.data,
                              mother_phone_no=form.mother_phone_no.data,
                              p_address=form.p_address.data,
                              l_address=form.l_address.data,
                              phone_no=form.phone_no.data,
                              dob=form.dob.data,
                              standard='1st',
                              religion=form.religion.data,
                              caste=form.caste.data,
                              gender=form.gender.data,
                              blood_group=form.blood_group.data,
                              profile_img=img,
                              admin=current_user)
            history = History(name_of_module=f'Added Student {form.fname.data} {form.lname.data}', activity='add',
                              admin=current_user)
            db.session.add(history)
            db.session.commit()

            db.session.add(student)
            db.session.commit()
            flash('Student added successfully', 'success')
            return redirect(url_for('all_students'))
    return render_template('add-student.html', title=f'{current_user.fname} {current_user.lname} account',
                           st1='Student', st2='Add Student', form=form, historys=historys)


@app.route("/student-details/<int:student_id>", methods=['GET', 'POST'])
@login_required
def student_details(student_id):
    student = Student.query.get_or_404(student_id)
    admin = Admin.query.filter_by(id=current_user.id).first_or_404()
    exams = Exam.query.filter_by(student=student, standard=student.standard)
    subjects = Subject.query.filter_by(admin=admin).all()
    subjects1 = Subject.query.filter_by(admin=admin, standard=student.standard).all()
    e = []
    for exam in exams:
        e.append(exam.subject.subject)
    e.sort()
    s = []
    for subject2 in subjects1:
        s.append(subject2.subject)
    s.sort()

    form = AddExamForm()
    form.subject.choices = [(subject.id, f'{subject.subject}({subject.standard})') for subject in subjects
                            if subject.standard == student.standard]

    if student.admin != current_user:
        flash("Sorry you can't view this student", 'danger')
        return redirect(url_for('all_students'))
    if form.validate_on_submit():
        sub = Subject.query.get(form.subject.data)
        subj = Exam.query.filter_by(student=student, standard=student.standard, subject=sub).first()
        if subj:
            flash("Sorry Student already have this subject, If You need to add new marks delete The subject and retry",
                  'warning')
        else:
            exam = Exam(subject=sub,
                        exam_name=f'{student.standard} Exam',
                        marks_opt=form.marks_opt.data,
                        standard=f'{student.standard}',
                        institution_name=form.institution_name.data,
                        subjects=[sub],
                        student=student)
            history = History(name_of_module=f'Added exam for {student.fname} {student.lname}', activity='add',
                              admin=current_user)
            db.session.add(history)
            db.session.commit()

            db.session.add(exam)
            db.session.commit()
            flash('Student Exam added successfully', 'success')
            return redirect(url_for('exam_view', student_id=student.id))
    promote = PromoteStudent()
    if promote.validate_on_submit():
        if student.standard == '1st':
            student.standard = '2nd'
        elif student.standard == '2nd':
            student.standard = '3rd'
        elif student.standard == '3rd':
            student.standard = '4th'
        elif student.standard == '4th':
            student.standard = '5th'
        elif student.standard == '5th':
            student.standard = '6th'
        elif student.standard == '6th':
            student.standard = '7th'
        elif student.standard == '7th':
            student.standard = '8th'
        elif student.standard == '8th':
            student.standard = '9th'
        elif student.standard == '9th':
            student.standard = '10th'
        db.session.commit()
        history = History(name_of_module=f'{student.fname} {student.lname} student promoted', activity='update',
                          admin=current_user)
        db.session.add(history)
        db.session.commit()

        flash('Student Exam added successfully', 'success')
        return redirect(url_for('student_details', student_id=student.id))
    return render_template('account-info.html', title='account',
                           st1='Account', st2='Student Account Info', student=student, form=form,
                           subjects=subjects, exams=exams,e=e,s=s,promote=promote)


@app.route("/student/<int:student_id>/update", methods=['GET', 'POST'])
@login_required
def student_update(student_id):
    student = Student.query.get_or_404(student_id)
    if student.admin != current_user:
        flash("Sorry you can't Update this student", 'danger')
        return redirect(url_for('all_students'))
    form = UpdateStudentForm()
    if form.validate_on_submit():
        if form.profile_img.data:
            picture_file1 = save_picture(form.profile_img.data)
            student.profile_img = picture_file1
        student.fname = form.fname.data
        student.father_name = form.father_name.data
        student.mother_name = form.mother_name.data
        student.lname = form.lname.data
        student.email = form.email.data
        student.roll_no = form.roll_no.data
        student.father_occupation = form.father_occupation.data
        student.mother_occupation = form.mother_occupation.data
        student.father_income = form.father_income.data
        student.mother_income = form.mother_income.data
        student.father_phone_no = form.father_phone_no.data
        student.mother_phone_no = form.mother_phone_no.data
        student.l_address = form.l_address.data
        student.p_address = form.p_address.data
        student.phone_no = form.phone_no.data
        student.dob = form.dob.data
        student.religion = form.religion.data
        student.caste = form.caste.data
        student.gender = form.gender.data
        student.blood_group = form.blood_group.data
        db.session.commit()
        history = History(name_of_module=f'Updated Student {form.fname.data} {form.lname.data}', activity='update',
                          admin=current_user)
        db.session.add(history)
        db.session.commit()
        flash('Account Updated Successfully', 'success')
        return redirect(url_for('all_students'))
    elif request.method == 'GET':
        form.fname.data = student.fname
        form.father_name.data = student.father_name
        form.mother_name.data = student.mother_name
        form.lname.data = student.lname
        form.email.data = student.email
        form.roll_no.data = student.roll_no
        form.father_occupation.data = student.father_occupation
        form.mother_occupation.data = student.mother_occupation
        form.father_income.data = student.father_income
        form.mother_income.data = student.mother_income
        form.father_phone_no.data = student.father_phone_no
        form.mother_phone_no.data = student.mother_phone_no
        form.p_address.data = student.p_address
        form.l_address.data = student.l_address
        form.phone_no.data = student.phone_no
        form.dob.data = student.dob
        form.religion.data = student.religion
        form.caste.data = student.caste
        form.gender.data = student.gender
        form.blood_group.data = student.blood_group
    return render_template('student-account-update.html', title='Account',
                           st1='Account', st2='Account Update', form=form)


@app.route("/all-students")
@login_required
def all_students():
    admin = Admin.query.filter_by(id=current_user.id).first_or_404()
    students = Student.query.filter_by(admin=admin)
    return render_template('all-students.html', title='All Students',
                           st1='Student', st2='All Student', students=students)

# @app.route("/student/<int:student_id>/delete", methods=['GET','POST'])
# @login_required
# def delete_student(student_id):
#     student = Student.query.get_or_404(student_id)
#     if student.admin != current_user:
#         flash("Sorry you can't Delete this student",'danger')
#         return redirect(url_for('dashboard'))
#     history = History(name_of_module=f'Deleted Student {student.fname} {student.lname}', activity='delete',
#                       admin=current_user)
#     db.session.add(history)
#     db.session.commit()
#     db.session.delete(student)
#     db.session.commit()
#     flash('Your student successfully Deleted', 'success')
#     return redirect(url_for('all_students'))
