from flask import Flask, Blueprint, render_template, request, render_template, redirect, url_for, session
from .models import Usuario, Municipio, Restaurantes, TipoComida, Productos, Orden
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
        direccion = request.form.get('direccion')
        if password != confirm_password:
            error = "Las contraseñas no coinciden"
            return render_template('signup.html', error=error)

        new_user = Usuario(
            nombre=first_name,
            apellido=last_name,
            celular=phone,
            direccion=direccion,
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
            session['user_id'] = str(user.id)
            return redirect('/location')
        else:
            error = 'Usuario o contraseña incorrectos'
            
    return render_template('signin.html', error=error)



@main.route('/location')
def location():
    error = None
    municipalities = None
    try:
        municipalities = Municipio.query.all()
    except Exception as e:
        error = "Error al registrar el usuario: " + str(e)
    return render_template('location.html', error=error, municipalities=municipalities)

@main.route('/site')
def site():
    error= None
    municipio_id = request.args.get('municipio')  # <-- GET parameter
    
    return render_template('site.html', error=error, municipio_id=municipio_id)


@main.route('/foodtype')
def foodtype():
    error= None
    municipio_id = request.args.get('municipio_id')  # <-- GET parameter
    site = request.args.get('site')  # <-- GET parameter
    tipoComida = []
    try:
        tipoComida = TipoComida.query.all()
    except Exception as e:
            error = "Error al obtener restaurantes: " + str(e)


    return render_template('food_type.html', error=error, municipio_id=municipio_id,site=site, tipoComida=tipoComida)


@main.route('/restaurant', methods=['GET', 'POST'])
def restaurant():
    error= None
    municipio_id = request.args.get('municipio_id') 
    site = request.args.get('site')
    tipoComida = request.args.getlist('tipoComida') 
    restaurantes = []
    try:
        query = Restaurantes.query.filter(Restaurantes.id_municipio == municipio_id)

        if site == "restaurante":
            query = query.filter(Restaurantes.consumo_en_sitio == True)
        else:
            query = query.filter(Restaurantes.delivery == True)

        if tipoComida:
            query = query.filter(
                Restaurantes.tipos_comida.any(TipoComida.id_tipo_comida.in_(tipoComida))
            )
        restaurantes = query.all()
    except Exception as e:
            error = "Error al obtener restaurantes: " + str(e)
    return render_template('select_restaurant.html', error=error, restaurantes=restaurantes)

@main.route('/dishes')
def dishes():
    error= None
    id_restaurante = request.args.get('restaurant') 
    platos = []
    try:
        platos = Productos.query.filter(Productos.id_restaurante == id_restaurante).all() 
    except Exception as e:
            error = "Error al obtener restaurantes: " + str(e)
    return render_template('dishes.html', error=error, platos=platos)


@main.route('/order')
def order():
    error= None
    dishes = request.args.getlist('dishes')
    user_id = session.get('user_id')
    print(user_id)
    platos = []
    try:
        platos = Productos.query.filter(Productos.id_producto.in_(dishes)).all()
        total = 0
        descripcion = ""

        for item in platos:
            total += item.precio
            descripcion += f"{item.nombre} : ${item.precio} \n"
        
        orden = Orden(
            precio_total = total,
            descripcion = descripcion,
            estado = 1,
            id_usuario= user_id
        )
        db.session.add(orden)
        db.session.commit()

    except Exception as e:
        error = "Error al obtener restaurantes: " + str(e)
        print(error)
    return render_template('order.html', error=error, platos=platos)



@main.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    session.clear()
    return redirect(url_for('main.admin_login'))