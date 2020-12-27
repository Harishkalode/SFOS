import pandas as pd
import os
import secrets
from flask import render_template, url_for, flash, redirect, request
from sfo import app, db
from sfo.forms import AddStudentForm, UpdateStudentForm, AddExamForm, PromoteStudent,AddStudentCSV
from sfo.models import Admin, Student, History, Subject, Exam
from flask_login import current_user, login_required
from sfo.routes import save_picture


def save_csv(from_csv):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(from_csv.filename)
    csv_fn = random_hex + f_ext
    csv_path = os.path.join(app.root_path, 'static/csv', csv_fn)
    from_csv.save(csv_path)
    return csv_fn


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
    promote = PromoteStudent()
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
        elif int(form.marks_opt.data) > int(sub.max_marks):
            flash('invalid data','warning')
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

    elif promote.validate_on_submit():
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


@app.route("/add-student/csv", methods=['GET', 'POST'])
def add_student_csv():
    form = AddStudentCSV()
    page = request.args.get('page', 1, type=int)
    admin = Admin.query.filter_by(id=current_user.id).first_or_404()
    historys = History.query.filter_by(admin=admin).order_by(History.date_created.desc()).paginate(page=page,
                                                                                                   per_page=5)
    if form.validate_on_submit():
        if form.file.data:
            csv_file=save_csv(form.file.data)
            df = pd.read_csv(f'sfo/static/csv/{csv_file}')
            a = pd.DataFrame(df)
            length_of_col = len(df.columns)
            length_of_row = len(df)
            missing_data = []
            duplicate_data = []

            if len(df.columns) == 20:
                for aa in range(0, length_of_col):
                    for miss in df[df.columns[aa]].isnull():
                        if miss:
                            missing_data.append('missing data')
                            break

                for dupli in a.duplicated(a.columns[4]):
                    if dupli:
                        duplicate_data.append('Duplicate Data')
                        break

                for dupli in df[df.columns[4]]:
                    email = Student.query.filter_by(admin=admin, email=dupli).first()
                    if email:
                        duplicate_data.append('Duplicate Data')

                for dupli in a.duplicated(a.columns[8]):
                    if dupli:
                        duplicate_data.append('Duplicate Data')
                        break
                for dupli in df[df.columns[8]]:
                    father_phone_no = Student.query.filter_by(admin=admin, father_phone_no=dupli).first()
                    if father_phone_no:
                        duplicate_data.append('Duplicate Data')

                for dupli in a.duplicated(a.columns[11]):
                    if dupli:
                        duplicate_data.append('Duplicate Data')
                        break

                for dupli in df[df.columns[11]]:
                    mother_phone_no = Student.query.filter_by(admin=admin, mother_phone_no=dupli).first()
                    if mother_phone_no:
                        duplicate_data.append('Duplicate Data')

                for dupli in a.duplicated(a.columns[14]):
                    if dupli:
                        duplicate_data.append('Duplicate Data')
                        break
                for dupli in df[df.columns[14]]:
                    phone_no = Student.query.filter_by(admin=admin, phone_no=dupli).first()
                    if phone_no:
                        duplicate_data.append('Duplicate Data')
                if 'missing data' not in missing_data:

                    if df.dtypes[0] == object and df.dtypes[1] == object and df.dtypes[2] == object and df.dtypes[3] == object \
                            and df.dtypes[4] == object and df.dtypes[5] == 'int64' and df.dtypes[6] == object \
                            and df.dtypes[7] == 'int64' and df.dtypes[8] == 'int64' and df.dtypes[9] == object \
                            and df.dtypes[10] == 'int64' and df.dtypes[11] == 'int64' and df.dtypes[12] == object \
                            and df.dtypes[13] == object and df.dtypes[14] == 'int64' and df.dtypes[15] == object \
                            and df.dtypes[16] == object and df.dtypes[17] == object and df.dtypes[18] == object \
                            and df.dtypes[19] == object:

                        if 'Duplicate Data' not in duplicate_data:
                            while True:
                                arr = []
                                for std in range(0, length_of_row):
                                    for stud in df.iloc[std]:
                                        arr.append(stud)

                                    student = Student(fname=arr[0],
                                                      father_name=arr[1],
                                                      mother_name=arr[2],
                                                      lname=arr[3],
                                                      email=arr[4],
                                                      roll_no=arr[5],
                                                      father_occupation=arr[6],
                                                      father_income=arr[7],
                                                      father_phone_no=arr[8],
                                                      mother_occupation=arr[9],
                                                      mother_income=arr[10],
                                                      mother_phone_no=arr[11],
                                                      p_address=arr[12],
                                                      l_address=arr[13],
                                                      phone_no=arr[14],
                                                      dob=arr[15],
                                                      standard='1st',
                                                      religion=arr[16],
                                                      caste=arr[17],
                                                      gender=arr[18],
                                                      blood_group=arr[19],
                                                      profile_img='default.png',
                                                      admin=current_user)
                                    db.session.add(student)
                                    db.session.commit()
                                    arr.clear()
                                break
                            os.unlink(os.path.join(app.root_path, 'static/csv', csv_file))
                        else:
                            flash('Duplicate Data','warning')
                            return redirect(url_for('add_student_csv'))
                    else:
                        os.unlink(os.path.join(app.root_path, 'static/csv', csv_file))
                        flash('Invalid Data Entry','warning')
                        return redirect(url_for('add_student_csv'))
                else:
                    flash('Missing Data please Fill Every Information','info')
                    return redirect(url_for('add_student_csv'))
            else:
                flash('Invalid Column length', 'warning')
                return redirect(url_for('add_student_csv'))
        flash('Student added successfully','success')
        return redirect(url_for('all_students'))
    return render_template('add-student-csv.html',title=f'{current_user.fname} {current_user.lname} account',
                           st1='Student', st2='Add Student',form=form, historys=historys)

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
