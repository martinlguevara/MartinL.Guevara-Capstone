import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv


# Cargar las variables de entorno desde un archivo .env (opcional)
load_dotenv()

app = Flask(__name__)

# Obtener la URL de la base de datos desde la variable de entorno DATABASE_URL
# Render debería tener configurada esta variable en su dashboard.
db_url = os.getenv('DATABASE_URL')

if db_url is None:
    raise ValueError("No se encontró la variable de entorno DATABASE_URL. Asegúrate de configurarla.")

# Configurar la conexión a la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar SQLAlchemy
db = SQLAlchemy(app)

# Modelo de Producto (ejemplo básico para CRUD)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)

# Crear tablas si no existen
@app.before_first_request
def create_tables():
    db.create_all()

# Rutas básicas para CRUD

# Obtener todos los productos
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price
    } for product in products])

# Crear un nuevo producto
@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    new_product = Product(name=data['name'], description=data['description'], price=data['price'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Producto agregado exitosamente'}), 201

# Obtener un producto por ID
@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'message': 'Producto no encontrado'}), 404
    return jsonify({
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price
    })

# Actualizar un producto por ID
@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'message': 'Producto no encontrado'}), 404
    data = request.get_json()
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    db.session.commit()
    return jsonify({'message': 'Producto actualizado exitosamente'})

# Eliminar un producto por ID
@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'message': 'Producto no encontrado'}), 404
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Producto eliminado exitosamente'})

# Ejecución principal
if __name__ == '__main__':
    app.run(debug=True)
