from flask import render_template, url_for, flash, redirect, request
from sfo import app, db
from sfo.forms import AddExamForm
from sfo.models import Admin, Student, Subject, History, Exam
from flask_login import current_user, login_required


@app.route("/exam/<int:student_id>/view", methods=['GET', 'POST'])
@login_required
def exam_view(student_id):
    student = Student.query.get_or_404(student_id)
    exams = Exam.query.filter_by(student=student,standard=student.standard)
    passed = []
    for pas in exams:
        if pas.marks_opt >= pas.subject.min_marks or pas.marks_opt == pas.subject.max_marks:
            passed.append(pas.marks_opt)
    a = len(passed)
    total = []
    for tot in exams:
        total.append(int(tot.marks_opt))
    t = sum(total)
    marks=[]
    for mark in exams:
        marks.append(int(mark.subject.max_marks))
    mm = sum(marks)
    if student.admin != current_user:
        flash("Sorry you can't view this student",'danger')
        return redirect(url_for('all_students'))
    percentage = (t/mm)*100.00
    perc = "{:.2f}".format(percentage)
    return render_template('exam.html',exams=exams,student=student,a=a,t=t,mm=mm,perc=perc,title=f'{student.fname} {student.lname} Exam',
                           st1=f'{student.fname} {student.lname}', st2=f'{student.standard} Exam')
