import secrets
import os
from flask import render_template, url_for, flash, redirect, request
from sfo import app, db, bcrypt, mail
from sfo.forms import RegistrationForm, LoginForm, RegistrationForm2, AccountUpdateForm, RequestResetForm,\
    ResetPasswordForm
from sfo.models import Admin, Student, Subject, History
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image
from flask_mail import Message



@app.route("/")
def home():
    return render_template('index.html')


@app.route("/admin-register", methods=['GET', 'POST'])
def admin_register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        admin = Admin(email=form.email.data, status='Head of Department', password=hashed_password)
        db.session.add(admin)
        db.session.commit()
        login_user(admin)
        history = History(name_of_module='Registration',activity='register',admin=current_user)
        db.session.add(history)
        db.session.commit()
        flash('Your Account has been created, You can now login', 'success')
        return redirect(url_for('register2'))
    return render_template('admin_register.html',form=form,title='Register')


@app.route('/register2',methods=['GET','POST'])
@login_required
def register2():
    form = RegistrationForm2()
    if form.validate_on_submit():
        current_user.fname = form.fname.data
        current_user.mname = form.mname.data
        current_user.lname = form.lname.data
        current_user.dob = form.dob.data
        current_user.institution_name = form.institution_name.data
        current_user.institution_email = form.institution_email.data
        current_user.phone_no = form.phone_no.data
        current_user.institution_address = form.institution_address.data
        current_user.institution_website_link = form.institution_website_link.data
        current_user.linkedin_link = form.linkedin_link.data
        current_user.instagram_link = form.instagram_link.data
        current_user.facebook_link = form.facebook_link.data
        db.session.commit()
        history = History(name_of_module='2 step Registration', activity='register', admin=current_user)
        db.session.add(history)
        db.session.commit()
        logout_user()
        return redirect(url_for('login'))
    return render_template('register2.html',form=form, title='Step two')


@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data).first()
        if admin and bcrypt.check_password_hash(admin.password, form.password.data):
            login_user(admin)
            history = History(name_of_module='Login', activity='login', admin=current_user)
            db.session.add(history)
            db.session.commit()
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        flash('Unsuccessful login', 'danger')
    return render_template('login.html', form=form, title='Login')


@app.route("/dashboard")
@login_required
def dashboard():
    admin = Admin.query.filter_by(id=current_user.id).first_or_404()
    students = Student.query.filter_by(admin=admin)
    subjects = Subject.query.filter_by(admin=admin)
    institute_subjects = Subject.query.filter_by(admin=admin,institute_subject='YES')
    no_of_student = students.count()
    no_of_subject = subjects.count()
    no_of_subject_inst = institute_subjects.count()
    page = request.args.get('page', 1, type=int)
    admin = Admin.query.filter_by(id=current_user.id).first_or_404()
    historys = History.query.filter_by(admin=admin).order_by(History.date_created.desc()).paginate(page=page,
                                                                                                   per_page=5)
    return render_template('dashboard.html',title='Dashboard', st1='Dashboard',no_of_student=no_of_student,
                           no_of_subject=no_of_subject,historys=historys,no_of_subject_inst=no_of_subject_inst)


@app.route("/history")
@login_required
def all_history():
    admin = Admin.query.filter_by(id=current_user.id).first_or_404()
    historys = History.query.filter_by(admin=admin)
    return render_template('all-history.html', title='All History',
                           st1='History', st2='All history',historys=historys)


@app.route("/account")
@login_required
def account_info():
    page = request.args.get('page', 1, type=int)
    admin = Admin.query.filter_by(id=current_user.id).first_or_404()
    historys = History.query.filter_by(admin=admin).order_by(History.date_created.desc()).paginate(page=page,
                                                                                                   per_page=5)
    return render_template('account-info.html', title=f'{current_user.fname} {current_user.lname} account',
                           st1='Account', st2='Account Info', a="a",historys=historys)


def save_picture(from_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(from_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (1000, 1000)
    i = Image.open(from_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account-update", methods=['GET', 'POST'])
@login_required
def account_update():
    form = AccountUpdateForm()
    if form.validate_on_submit():
        if form.profile_img.data:
            picture_file1 = save_picture(form.profile_img.data)
            current_user.profile_img = picture_file1
        if form.institution_logo.data:
            picture_file2 = save_picture(form.institution_logo.data)
            current_user.institution_logo = picture_file2
        current_user.email = form.email.data
        current_user.status = form.status.data
        current_user.fname = form.fname.data
        current_user.mname = form.mname.data
        current_user.lname = form.lname.data
        current_user.dob = form.dob.data
        current_user.institution_name = form.institution_name.data
        current_user.institution_email = form.institution_email.data
        current_user.phone_no = form.phone_no.data
        current_user.institution_address = form.institution_address.data
        current_user.institution_website_link = form.institution_website_link.data
        current_user.linkedin_link = form.linkedin_link.data
        current_user.instagram_link = form.instagram_link.data
        current_user.facebook_link = form.facebook_link.data
        db.session.commit()
        history = History(name_of_module='Account Update', activity='update', admin=current_user)
        db.session.add(history)
        db.session.commit()
        flash('Your Account Updated Successfully', 'success')
        return redirect(url_for('account_info'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.status.data = current_user.status
        form.fname.data = current_user.fname
        form.mname.data = current_user.mname
        form.lname.data = current_user.lname
        form.dob.data = current_user.dob
        form.institution_name.data = current_user.institution_name
        form.institution_email.data = current_user.institution_email
        form.phone_no.data = current_user.phone_no
        form.institution_address.data = current_user.institution_address
        form.institution_website_link.data = current_user.institution_website_link
        form.linkedin_link.data = current_user.linkedin_link
        form.instagram_link.data = current_user.instagram_link
        form.facebook_link.data = current_user.facebook_link
    return render_template('account-update.html',title=f'{current_user.fname} {current_user.lname} account',
                           st1='Account', st2='Account Update',form=form)


@app.route("/logout")
@login_required
def logout():
    history = History(name_of_module='Logout', activity='logout',
                      admin=current_user)
    db.session.add(history)
    db.session.commit()
    logout_user()
    return redirect(url_for('home'))


def send_reset_email(admin):
    token = admin.get_reset_token()
    msg = Message('Password reset request',
                  sender='harish.kalode@gmail.com',
                  recipients=[admin.email])
    msg.body = f"""
To reset your password, click on the given link :
{url_for('reset_token', token=token, _external=True)}

If you did not make this request Please ignore this and no changes will be done
    """
    mail.send(msg)


@app.route("/reset-password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for('reset_password'))
    form = RequestResetForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data).first()
        send_reset_email(admin)
        flash('Email has sent on your account to reset the password','success')
        return redirect(url_for('login'))
    return render_template('reset-request.html', title='Reset Password', form=form)


@app.route("/reset-password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:   
        logout_user()
        return redirect(url_for('reset_password'))
    admin = Admin.verify_reset_token(token)
    if admin is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        admin.password = hashed_password
        db.session.commit()
        login_user(admin)
        history = History(name_of_module='Password Updated', activity='update',
                          admin=current_user)
        db.session.add(history)
        db.session.commit()
        flash('Your password has been updated, You can now login', 'success')
        return redirect(url_for('dashboard'))
    return render_template('reset-password.html', title='Reset Password', form=form)


@app.errorhandler(401)
def page_not_found(e):
    # note that we set the 401 status explicitly
    return render_template('401.html'), 401


@app.errorhandler(403)
def page_not_found(e):
    # note that we set the 403 status explicitly
    return render_template('403.html'), 403


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    # note that we set the 500 status explicitly
    return render_template('500.html'), 500
