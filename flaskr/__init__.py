import os
from flask import Flask
from flask import flash, render_template, request, redirect


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def login():
        return render_template('auth/login.html')

        
        # a simple page that says hello
    @app.route('/forget-password')
    def forget_password():
        return render_template('auth/forgot-password.html')

        # a simple page that says hello
    @app.route('/sing-up')
    def sing_up():
        return render_template('auth/sign-up.html')
        
    @app.route('/dashboard')
    def dashboard():
        return render_template('admin/dashboard.html')
    return app