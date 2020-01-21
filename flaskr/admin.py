import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

app = Blueprint('admin', __name__, url_prefix='/admin')

@app.route('/dashboard')
def dashboard():
    return render_template('admin/dashboard.html')


@app.route('/etenders')
def etenders():
    return render_template('admin/etenders.html')
