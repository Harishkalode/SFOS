from flask import render_template, url_for, flash, redirect, request
from sfo import app, db,graph
from sfo.forms import AddExamForm, StudentExamView
from sfo.models import Admin, Student, Subject, History, Exam
from flask_login import current_user, login_required
import dash
import dash_core_components as dcc
import dash_html_components as html


@app.route("/exam/<int:student_id>/view", methods=['GET', 'POST'])
@login_required
def exam_view(student_id):
    student = Student.query.get_or_404(student_id)
    exams = Exam.query.filter_by(student=student,standard=student.standard)
    exams2 = Exam.query.filter_by(student=student)
    exam3 = []
    for exam in exams2:
        if exam.standard not in exam3:
            exam3.append(exam.standard)
    form = StudentExamView()
    form.standard.choices = [(exam, f'{exam} standard ') for exam in exam3]
    if form.validate_on_submit():
        exams = Exam.query.filter_by(student=student, standard=form.standard.data)
        return exams
    elif request.method == 'GET':
        form.standard.data = student.standard
    passed = []
    for pas in exams:
        if int(pas.marks_opt) >= int(pas.subject.min_marks) or int(pas.marks_opt) == int(pas.subject.max_marks):
            passed.append(pas.marks_opt)
    a = len(passed)
    total = []
    for tot in exams:
        total.append(int(tot.marks_opt))
    t = sum(total)
    max_marks=[]
    for mark in exams:
        max_marks.append(int(mark.subject.max_marks))
    mm = sum(max_marks)
    if student.admin != current_user:
        flash("Sorry you can't view this student",'danger')
        return redirect(url_for('all_students'))
    percentage = (t/mm)*100.00
    perc = "{:.2f}".format(percentage)

    subjects=[]
    for subject in exams:
        subjects.append(subject.subject.subject)

    marks = []
    for mark1 in exams:
        marks.append(int(mark1.marks_opt))

    graph.layout = dcc.Graph(
                id='#samplechart',
                figure={
                    'data': [
                        {'x': subjects, 'y':marks,'type':'line','name':'First Chart'}
                    ],
                    'layout':{
                        'title': 'Simple Bar Chart'
                    }
                }
            )

    return render_template('exam.html',exams=exams,student=student,a=a,t=t,mm=mm,perc=perc,title=f'{student.fname} {student.lname} Exam',
                           st1=f'{student.fname} {student.lname}', st2='Exam',form=form)


@app.route("/exam/<int:exam_id>/delete", methods=['GET','POST'])
@login_required
def delete_exam(exam_id):
    exam = Exam.query.get_or_404(exam_id)
    if exam.student.admin != current_user:
        flash("Sorry you can't Delete this student",'danger')
        return redirect(url_for('all_student'))
    history = History(name_of_module=f'Deleted Exam for Student {exam.student.fname} {exam.student.lname}',
                      activity='delete', admin=current_user)
    db.session.add(history)
    db.session.commit()
    db.session.delete(exam)
    db.session.commit()
    flash('Your student successfully Deleted', 'success')
    return redirect(url_for('all_students'))
