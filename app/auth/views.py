from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user, login_required, current_user
from . import auth
from .. models import User
from . forms import LoginForm
from . forms import RegistrationForm
from .. email import send_email
from .. import db

import pydevd


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # pydevd.settrace('192.168.56.1', port=22, stdoutToServer=True, stderrToServer=True)
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # ipdb.set_trace()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    # pydevd.settrace('192.168.56.1', port=22, stdoutToServer=True, stderrToServer=True)
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    # pydevd.settrace('192.168.56.1', port=22, stdoutToServer=True, stderrToServer=True)
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account', 'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    # pydevd.settrace('192.168.56.1', port=22, stdoutToServer=True, stderrToServer=True)
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@auth.before_app_request
def before_request():
    # pydevd.settrace('192.168.56.1', port=22, stdoutToServer=True, stderrToServer=True)

    endpoint = 'None'
    if request.endpoint:
        endpoint = request.endpoint[:5]

    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed and endpoint not in ['auth.', 'static', 'main.']:
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    # pydevd.settrace('192.168.56.1', port=22, stdoutToServer=True, stderrToServer=True)
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/confirm')
@login_required
def resend_confirmation():
    # pydevd.settrace('192.168.56.1', port=22, stdoutToServer=True, stderrToServer=True)
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))