import uuid
from sqlalchemy.dialects.postgresql import UUID
from . import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<Usuario {self.nombre}>'
