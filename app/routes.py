from flask import Flask, Blueprint, render_template, request, render_template, redirect, url_for, session
from .models import Usuario
main = Blueprint('main', __name__)

@main.route("/")
def home():
    return render_template("index.html")


@main.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = Usuario.query.filter_by(celular=username, password=password, tipo_usuario=1).first()
        if user:
            session['admin_logged_in'] = True
            return redirect('/admin')
        else:
            error = 'Usuario o contraseña incorrectos'
            
    return render_template('admin_login.html', error=error)

@main.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('main.admin_login'))