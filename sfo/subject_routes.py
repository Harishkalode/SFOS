from flask import render_template, url_for, flash, redirect, request
from sfo import app, db
from sfo.forms import AddSubjectForm, UpdateSubjectForm
from sfo.models import Admin, Subject, History
from flask_login import current_user, login_required


@app.route("/subject/new", methods=['GET', 'POST'])
@login_required
def add_subject():
    form = AddSubjectForm()
    page = request.args.get('page', 1, type=int)
    admin = Admin.query.filter_by(id=current_user.id).first_or_404()
    historys = History.query.filter_by(admin=admin).order_by(History.date_created.desc()).paginate(page=page,
                                                                                                   per_page=5)
    if form.validate_on_submit():
        subject = Subject(subject=form.subject.data,
                          standard=form.standard.data,
                          min_marks=form.min_marks.data,
                          max_marks=form.max_marks.data,
                          institute_subject=form.institute_subject.data,
                          admin=current_user)
        history = History(name_of_module=f'Added Subject {form.subject.data}', activity='add',
                          admin=current_user)
        db.session.add(history)
        db.session.commit()

        db.session.add(subject)
        db.session.commit()
        flash('Subject added successfully', 'success')
        return redirect(url_for('all_subjects'))
    return render_template('add-subject.html', title='Add Subject',
                           st1='Subject', st2='Add subject',form=form,historys=historys)


@app.route("/subject-details/<int:subject_id>")
@login_required
def subject_details(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    page = request.args.get('page', 1, type=int)
    admin = Admin.query.filter_by(id=current_user.id).first_or_404()
    historys = History.query.filter_by(admin=admin).order_by(History.date_created.desc()).paginate(page=page,
                                                                                                   per_page=5)
    if subject.admin != current_user:
        flash("Sorry you can't view this subject",'danger')
        return redirect(url_for('all_subject'))
    return render_template('subject-info.html', title='Subject',
                           st1='subject', st2='subject Info',subject=subject,historys=historys)


@app.route("/all-subjects")
@login_required
def all_subjects():
    admin = Admin.query.filter_by(id=current_user.id).first_or_404()
    subjects = Subject.query.filter_by(admin=admin)
    return render_template('all-subject.html', title='All Subjects',
                           st1='Subject', st2='All Subject',subjects=subjects)


@app.route("/subject/<int:subject_id>/update", methods=['GET', 'POST'])
@login_required
def subject_update(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    page = request.args.get('page', 1, type=int)
    admin = Admin.query.filter_by(id=current_user.id).first_or_404()
    historys = History.query.filter_by(admin=admin).order_by(History.date_created.desc()).paginate(page=page,
                                                                                                   per_page=5)
    if subject.admin != current_user:
        flash("Sorry you can't Update this subject",'danger')
        return redirect(url_for('all_subjects'))
    form = UpdateSubjectForm()
    if form.validate_on_submit():
        subject.subject = form.subject.data
        subject.standard = form.standard.data
        subject.min_marks = form.min_marks.data
        subject.max_marks = form.max_marks.data
        subject.institute_subject = form.institute_subject.data
        db.session.commit()
        history = History(name_of_module=f'Updated Subject {form.subject.data}', activity='update',
                          admin=current_user)
        db.session.add(history)
        db.session.commit()
        flash('Subject Updated Successfully', 'success')
        return redirect(url_for('all_subjects'))
    elif request.method == 'GET':
        form.subject.data = subject.subject
        form.standard.data = subject.standard
        form.max_marks.data = subject.max_marks
        form.min_marks.data = subject.min_marks
        form.institute_subject.data = subject.institute_subject
    return render_template('subject-update.html', title='Subject Update',
                           st1='Subject', st2='Subject Update', form=form,subject=subject,historys=historys)


@app.route("/subject/<int:subject_id>/delete", methods=['POST'])
@login_required
def delete_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    if subject.admin != current_user:
        flash("Sorry you can't Delete this subject",'danger')
        return redirect(url_for('dashboard'))
    history = History(name_of_module=f'Deleted Subject {subject.subject}', activity='delete',
                      admin=current_user)
    db.session.add(history)
    db.session.commit()

    db.session.delete(subject)
    db.session.commit()
    flash('Your subject successfully Deleted', 'success')
    return redirect(url_for('all_subjects'))