import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db
import json
bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db['test'].find({name:'amit'}).text is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/sign-up.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':        
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        
        error = None        
        users = db['form_f_2017'].find()
        # for record in users:
        #     print(record)

        json.dumps(users)
        return render_template('test.html',records=users)
        # if error is None:
        #     session.clear()
        #     #session['user_id'] = users['id']
        #     return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/login.html')


@bp.route('/forget-password')
def forgot_password():
    return render_template('auth/forget-password.html')
