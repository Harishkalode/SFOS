from flask import render_template, url_for, flash, redirect, request
from sfo import app, db
from sfo.forms import AddExamForm
from sfo.models import Admin, Student, Subject, History, Exam
from flask_login import current_user, login_required


@app.route("/exam/<int:student_id>/view", methods=['GET', 'POST'])
@login_required
def exam_view(student_id):
    student = Student.query.get_or_404(student_id)
    exams = Exam.query.filter_by(student=student).all()
    if student.admin != current_user:
        flash("Sorry you can't view this student",'danger')
        return redirect(url_for('all_students'))
    return render_template('exam.html',exams=exams,student=student)
