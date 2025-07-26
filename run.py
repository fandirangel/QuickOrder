import os
from app import create_app  # Asegúrate de que "app" sea el nombre de tu paquete

# Creamos la app usando tu factory
app = create_app()

if __name__ == "__main__":
    # Activa el modo debug y el recargador automático
    app.run(
        debug=True,
        host="0.0.0.0",  # Para permitir conexiones externas (opcional)
        port=int(os.environ.get("PORT", 5000))  # Usa el puerto 5000 por defecto
    )
