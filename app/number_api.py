from flask import jsonify, request, Response
import jwt

from settings import app
from number_models import DIDNumber
from auth_models import User
from auth_api import token_required


@app.route('/')
@app.route('/dids', methods=['GET'])
@token_required
def get_dids(current_user):
    if(current_user):
        return jsonify({
            'DID Numbers': DIDNumber.get_all_dids()
        })

@app.route('/dids/<int:id>', methods=['GET'])
@token_required
def get_did_by_id(current_user, id):
    if(current_user):
        return_value = DIDNumber.get_did(id)
        return jsonify(return_value)

@app.route('/dids', methods=['POST'])
@token_required
def add_did(current_user):
    if(current_user):
        request_data = request.get_json()

        DIDNumber.add_did(
            request_data["value"],
            request_data["monthyPrice"],
            request_data["setupPrice"],
            request_data["currency"]
        )

        response = Response("DID number added", 201, mimetype='application/json')
        return response

@app.route('/dids/<int:id>', methods=['PUT'])
@token_required
def update_did(current_user, id):
    if(current_user):
        request_data = request.get_json()
        DIDNumber.update_did(
            id,
            request_data["value"],
            request_data["monthyPrice"],
            request_data["setupPrice"],
            request_data["currency"]
        )
        response = Response("DID number updated", status=200, mimetype='application/json')
        return response

@app.route('/dids/<int:id>', methods=['DELETE'])
@token_required
def remove_did(current_user, id):
    if(current_user):
        DIDNumber.delete_did(id)
        response = Response("DID number deleted", status=200, mimetype='application/json')
        return response


if __name__ == "__main__":
    app.run(port=1234)
