from flask import request, jsonify, make_response, Response
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
import datetime
from functools import wraps

from settings import app, db
from auth_models import User


def token_required(f):
    """
    This method ensures access only if the token is valid

    Returns:
        json: {'message': '...'} if the token is invalid or missing
        function: otherwise
    """
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'token is invalid'})

        return f(*args, **kwargs)
    return decorator


@app.route('/register', methods=['GET', 'POST'])
def signup_user():
    """
    This method signs up an user and adds in the database
    Returns:
        json
    """
    data = request.get_json()

    hashed_password = generate_password_hash(
        data['password'],
        method='sha256'
    )

    new_user = User(
        public_id=str(uuid.uuid4()),
        name=data['name'],
        password=hashed_password
    )
    db.session.add(new_user)
    db.session.commit()

    response = Response(
        "registered successfully",
        201,
        mimetype='application/json'
    )
    return response

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    """
    This method connects an user and adds in the database
    Returns:
        make_response (json):  status 401 - if ant credentials is missing
        responseObject (json): status 200 and token - if the credentials exist
                               and are correct
    """
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response(
            'could not verify',
            401,
            {'WWW.Authentication': 'Basic realm: "login required"'}
    )

    user = User.query.filter_by(name=auth.username).first()

    if check_password_hash(user.password, auth.password):
        token = jwt.encode(
            {
            'public_id': user.public_id,
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=120)
            },
            app.config['SECRET_KEY']
        )
        responseObject = jsonify({'token' : token.decode('UTF-8')})
        return make_response(responseObject), 200

    return make_response(
        'could not verify',
        401,
        {'WWW.Authentication': 'Basic realm: "login required"'}
    )

@app.route('/users', methods=['GET'])
def get_all_users():
    """
    This method gets all users
    Returns:
        make_response (json): status 200 - if users are obtained
    """
    users = User.query.all()

    result = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password

        result.append(user_data)
    return make_response(jsonify({'users': result})), 200

@app.route('/remove_user/<public_id>', methods=['DELETE'])
@token_required
def remove_user(public_id):
    """
    This method removes an user
    Returns:
        response (json): status 200 - if the user was deleted
    """
    User.query.filter_by(public_id=str(public_id)).delete()
    db.session.commit()
    response = Response(
        "User deleted",
        status=200,
        mimetype='application/json'
    )
    return response
