from . import app, db, logger

from flask import jsonify
from flask_jwt_extended import jwt_required
from .models import Customer, customer_schema


@app.route('/')
def index():
    return jsonify({'message': 'Welcome to the Flask API'})

@app.route('/register', methods=['POST'])
def register():
    json_data = request.get_json()

    # Validate and deserialize input
    try:
        data = user_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    # Check if user already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"message": "Username already taken"}), 409

    # Create new user
    user = User(username=data['username'])
    user.password = data['password']  # This sets the password hash
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully", "user_id": user.id}), 201

@app.route('/customers', methods=['GET'])
@jwt_required()
def get_customers():
    query = Customer.query
    name = request.args.get('name')
    phone = request.args.get('phone')
    state = request.args.get('state')
    if name:
        query = query.filter_by(name=name)
    if phone:
        query = query.filter_by(phone=phone)
    if state:
        query = query.filter(state=state)
    items = query.all()
    return jsonify([item.serialize() for item in items])

@app.route('/customers/<int:item_id>', methods=['GET'])
@jwt_required()
def get_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    return jsonify({'name': customer.name, 'phone': customer.phone, 'state': customer.state})

@app.route('/customers', methods=['POST'])
@jwt_required()
def create_customer():
    json_input = request.get_json()
    try:
        data = customer_schema.load(json_input)
    except ValidationError as err:
        return jsonify(err.messages), 400
    new_customer = Customer(**data)
    db.session.add(new_customer)
    db.session.commit()
    return jsonify(customer_schema.dump(new_customer)), 201

@app.route('/customers/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': 'Customer deleted'}), 200

@app.route('/customers/search', methods=['GET'])
@jwt_required()
def search_customers():
    keyword = request.args.get('keyword', '')
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    query = Customer.query.filter(Customer.name.ilike(f'%{keyword}%'))
    results = query.paginate(page=page, per_page=limit, error_out=False)
    customers = results.items
    return jsonify({'customers': [customer.name for customer in customers], 'total': results.total})

@app.route('/customers/<int:id>', methods=['PUT'])
@jwt_required()
def update_customer(id):
    customer = Customer.query.get_or_404(id)
    json_input = request.get_json()
    try:
        data = customer_schema.load(json_input)
    except ValidationError as err:
        return jsonify(err.messages), 400
    for key, value in data.items():
        setattr(customer, key, value)
    db.session.commit()
    return jsonify(customer_schema.dump(customer))



@app.errorhandler(404)
def not_found_error(error):
    logger.error(error)
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f'Internal Error: {error}')
    return jsonify({'error': 'Internal server error'}), 500

@app.before_request
def before_request_logging():
    if request.method in ['POST', 'PUT', 'DELETE']:
        logger.info(f'Handling {request.method} request for {request.url}: {request.get_json()}')

@app.after_request
def after_request_logging(response):
    logger.info(f'Response for {request.method} request to {request.url}: {response.status_code}')
    return response