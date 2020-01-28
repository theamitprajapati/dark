import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flaskr.db import get_db

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/dashboard')
def dashboard():
    return render_template('admin/dashboard.html')


@bp.route('/etenders')
def etenders():
    return render_template('admin/etenders.html')
