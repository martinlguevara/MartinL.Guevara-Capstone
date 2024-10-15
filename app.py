from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Crear la aplicación Flask
app = Flask(__name__)

# Configurar la URL de la base de datos desde la variable de entorno
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

# Desactivar el seguimiento de modificaciones para mejorar el rendimiento
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos
db = SQLAlchemy(app)

# Definir un modelo de ejemplo (Producto)
class Producto(db.Model):
    __tablename__ = 'productos'  # Nombre de la tabla en la base de datos
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Producto {self.nombre}>'

# Ruta de ejemplo
@app.route('/')
def home():
    return '¡Bienvenido a la aplicación de productos!'

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
