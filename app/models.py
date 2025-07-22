import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
from . import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=True)
    celular = db.Column(db.String(13), nullable=False)
    password = db.Column(db.String(13), nullable=False)
    usuario_verificado = db.Column(db.Boolean(), default=False, nullable=False)
    fecha_creacion = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    tipo_usuario = db.Column(db.Integer, nullable=False)
    
class Orden(db.Model):
    __tablename__ = "orden"

    id_orden = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    precio_total = db.Column(db.Float(precision=2), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    estado = db.Column(db.Integer, nullable=False)
    id_usuario = db.Column(UUID(as_uuid=True), db.ForeignKey('usuarios.id'), nullable=False)


class Departamento(db.Model):
    __tablename__ = "departamento"

    id_departamento = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo = db.Column(db.Integer, nullable=False)
    nombre = db.Column(db.String(50), nullable=False)

# class Ciudad(db.Model):
#     __tablename__ = "ciudad"

#     id_ciudad = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     codigo = db.Column(db.Integer, nullable=False)
#     nombre = db.Column(db.String(50), nullable=False)
#     id_departamento = db.Column(UUID(as_uuid=True), db.ForeignKey('departamento.id_departamento'), nullable=False)
#     ciudad = db.relationship('Ciudad', backref='municipio')

class Municipio(db.Model):
    __tablename__ = "municipio"

    id_municipio = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo = db.Column(db.Integer, nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    id_departamento = db.Column(UUID(as_uuid=True), db.ForeignKey('departamento.id_departamento'), nullable=False)
    departamento = db.relationship('Departamento', backref='municipio')

class Restaurantes(db.Model):
    __tablename__ = "restaurantes"

    id_restaurante = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = db.Column(db.String(200), nullable=False)
    rango_precios = db.Column(db.String(50), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    tiempo_estimado = db.Column(db.Integer, nullable=False)
    id_municipio = db.Column(UUID(as_uuid=True), db.ForeignKey('municipio.id_municipio'), nullable=False)
    municipio = db.relationship('Municipio', backref='restaurantes')
    consumo_en_sitio = db.Column(db.Boolean(), default=False, nullable=False)
    delivery = db.Column(db.Boolean(), default=False, nullable=False)
    tipos_comida = db.relationship(
        "TipoComida",
        secondary="restauranteTipoComida",
        backref="restaurantes",
        lazy="joined"
    )
    
class TipoComida(db.Model):
    __tablename__ = "tipoComida"

    id_tipo_comida = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    descripcion = db.Column(db.String(300), nullable=False)
    
    def __repr__(self):
        return self.descripcion

class RestauranteTipoComida(db.Model):
    __tablename__ = "restauranteTipoComida"

    id_restaurante = db.Column(UUID(as_uuid=True), db.ForeignKey('restaurantes.id_restaurante'), primary_key=True, nullable=False)
    id_tipo_comida = db.Column(UUID(as_uuid=True), db.ForeignKey('tipoComida.id_tipo_comida'), primary_key=True, nullable=False)

class Productos(db.Model):
    __tablename__ = "productos"

    id_producto = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_restaurante = db.Column(UUID(as_uuid=True), db.ForeignKey('restaurantes.id_restaurante'), nullable=False)
    nombre = db.Column(db.String(200), nullable=False)
    precio = db.Column(db.Float(precision=2), nullable=False)
    descripcion = db.Column(db.String(300), nullable=False)
    imagen = db.Column(db.String(200))


class OrdenDetalles(db.Model):
    __tablename__ = "ordenDetalles"

    id_orden_detalle = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_orden = db.Column(UUID(as_uuid=True), db.ForeignKey('orden.id_orden'), nullable=False)
    id_producto = db.Column(UUID(as_uuid=True), db.ForeignKey('productos.id_producto'), nullable=False)

class Subproductos(db.Model):
    __tablename__ = "subproductos"

    id_subproducto = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = db.Column(db.String(200), nullable=False)
    precio = db.Column(db.Float(precision=2), nullable=False)
    descripcion = db.Column(db.String(300), nullable=False)
    valor_adicion = db.Column(db.Float(precision=2), nullable=False)
    valor_remocion = db.Column(db.Float(precision=2), nullable=False)

class OrdenDetallePersonalizacion(db.Model):
    __tablename__ = "ordenDetallePersonalizacion"

    id_orden_detalle_personalizacion = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_orden_detalle = db.Column(UUID(as_uuid=True), db.ForeignKey('ordenDetalles.id_orden_detalle'), nullable=False)
    id_subproducto = db.Column(UUID(as_uuid=True), db.ForeignKey('subproductos.id_subproducto'), nullable=False)
    accion = db.Column(db.Integer, nullable=False)
    ajuste_precio = db.Column(db.Float(precision=2), nullable=False)

class ProductosSubproductos(db.Model):
    __tablename__ = "productosSubproductos"

    id_producto = db.Column(UUID(as_uuid=True), db.ForeignKey('productos.id_producto'), primary_key=True, nullable=False)
    id_subproducto = db.Column(UUID(as_uuid=True), db.ForeignKey('subproductos.id_subproducto'), primary_key=True, nullable=False)
    
class OpinionUsuarios(db.Model):
    __tablename__ = "opinionUsuarios"

    id_restaurante = db.Column(UUID(as_uuid=True), db.ForeignKey('restaurantes.id_restaurante'), primary_key=True, nullable=False)
    cumple_tiempo_estimado = db.Column(db.Boolean(), nullable=False)
    calificacion =  db.Column(db.Integer, nullable=False)
    id_usuario = db.Column(UUID(as_uuid=True), db.ForeignKey('usuarios.id'), primary_key=True, nullable=False)
