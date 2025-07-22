from flask import Flask, request, render_template, redirect, url_for, session
from markupsafe import Markup
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_admin import Admin
from flask_admin import AdminIndexView
from flask_admin.menu import MenuLink
from flask_admin.contrib.sqla import ModelView
from wtforms_sqlalchemy.fields import QuerySelectMultipleField, QuerySelectField
from flask_admin.form import ImageUploadField
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY','Rr_123456')
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from .models import Usuario, Restaurantes, TipoComida, Departamento, Municipio, Productos, ProductosSubproductos
    from .routes import main 

    class MunicipioAdmin(ModelView):
        #form_excluded_columns = ('id_municipio', )
        form_columns = ['codigo', 'nombre', 'departamento']

        form_overrides = {
            'departamento': QuerySelectField
        }
        form_args = {
            'departamento': {
            'query_factory': lambda: Departamento.query.all(),
            'get_label': 'nombre'
            }
        }
        
    
    class RestauranteAdmin(ModelView):
        form_columns = ['nombre', 'rango_precios', 'direccion','tiempo_estimado', 'municipio', 'consumo_en_sitio','delivery','tipos_comida']

        form_overrides = {
            'tipos_comida': QuerySelectMultipleField,
            'municipio': QuerySelectField
        }
        form_args = {
            'tipos_comida': {
                'query_factory': lambda: TipoComida.query.all(),
                'get_label': 'descripcion'
            },
            'municipio': {
            'query_factory': lambda: Municipio.query.all(),
            'get_label': 'nombre'
            }
        }
    class TipoComidaAdmin(ModelView):
        form_columns = ['descripcion']  # Solo el campo que quieres
        form_overrides = {}  # Limpio
        form_args = {
            'municipio': {
                'query_factory': lambda: Municipio.query.all(),
                'get_label': 'nombre'
                }
        }  
    class UsuarioAdmin(SecureModelView):
        form_choices = {
            'tipo_usuario': [
                (1, 'Admin'),
                (2, 'Cliente'),
                (3, 'Otro')
            ]
        }
    
    class ProductoAdmin(ModelView):
        form_columns = ['restaurante','nombre', 'precio','descripcion', 'imagen']
        # Personaliza el campo imagen para que permita subir archivos
        form_extra_fields = {
            'imagen': ImageUploadField('Imagen del porducto',
                base_path=os.path.join(os.getcwd(), 'static', 'uploads'),
                relative_path='uploads/',
                url_relative_path='static/uploads/')
        }
        form_overrides = {
            'restaurante': QuerySelectField
        }
        # Configuramos el comportamiento del SelectField
        form_args = {
            'restaurante': {
                'query_factory': lambda: Restaurantes.query.all(),
                'get_label': 'nombre'
            }
        }

    # Flask-Admin
    admin = Admin(app, name='Panel Admin', template_mode='bootstrap3', index_view=MyAdminIndexView())
    admin.add_view(UsuarioAdmin(Usuario, db.session))
    admin.add_view(RestauranteAdmin(Restaurantes, db.session))
    admin.add_view(TipoComidaAdmin(TipoComida, db.session))
    admin.add_view(ModelView(Departamento, db.session))
    admin.add_view(MunicipioAdmin(Municipio, db.session))
    #admin.add_view(ModelView(Productos, db.session))
    admin.add_view(ProductoAdmin(Productos, db.session))
    admin.add_view(ModelView(ProductosSubproductos, db.session))

    admin.add_link(MenuLink(name='Cerrar sesion', category='', url='/admin/logout'))
    app.register_blueprint(main) 

    if __name__ == '__main__':
     app.run(debug=True)
    return app


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return session.get('admin_logged_in')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.admin_login'))


class SecureModelView(ModelView):
    def is_accessible(self):
        return session.get('admin_logged_in')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.admin_login'))
    
    def render (self, template, **kwargs):
        kwargs['logout_button'] = Markup('<a class="btn btn-danger" href="/admin/logout">Cerrar sesión</a>')
        return super().render(template, **kwargs)
    
