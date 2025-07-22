from flask import Flask, Blueprint, render_template, request, render_template, redirect, url_for, session
from .models import Usuario, Municipio, Restaurantes
from app import db

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

@main.route('/sign')
def sign():
    return render_template('sign.html')


@main.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        first_name = request.form.get('name')
        last_name = request.form.get('lastname')
        phone = request.form.get('phone')
        password = request.form.get('password')
        confirm_password = request.form.get('confirmpassword')

        if password != confirm_password:
            error = "Las contraseñas no coinciden"
            return render_template('signup.html', error=error)

        new_user = Usuario(
            nombre=first_name,
            apellido=last_name,
            celular=phone,
            password=password,
            tipo_usuario=2
        )
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/signin')
        except Exception as e:
            db.session.rollback()
            error = "Error al registrar el usuario: " + str(e)

            
    return render_template('signup.html', error=error)


@main.route('/signin', methods=['GET', 'POST'])
def signin():
    error = None
    if request.method == 'POST':
        username = request.form['phone']
        password = request.form['password']

        user = Usuario.query.filter_by(celular=username, password=password).first()
        if user:
            session['admin_logged_in'] = True
            return redirect('/location')
        else:
            error = 'Usuario o contraseña incorrectos'
            
    return render_template('signin.html', error=error)

@main.route('/restaurant', methods=['GET', 'POST'])
def restaurant():
    error= None
    municipio_id = request.args.get('municipio')  # <-- GET parameter
    restaurantes = []
    if municipio_id:
        try:
            # Query all restaurants for that municipio
            restaurantes = Restaurantes.query.filter_by(id_municipio=municipio_id).all()
        except Exception as e:
            error = "Error al obtener restaurantes: " + str(e)
    
    return render_template('select_restaurant.html', error=error, restaurantes=restaurantes)

@main.route('/location')
def location():
    error = None
    municipalities = None
    try:
        municipalities = Municipio.query.all()
    except Exception as e:
        error = "Error al registrar el usuario: " + str(e)
    return render_template('location.html', error=error, municipalities=municipalities)


@main.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('main.admin_login'))