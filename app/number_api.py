from flask import jsonify, request, Response
import jwt

from settings import app
from number_models import DIDNumber
from auth_models import User
from auth_api import token_required



@app.route('/')
@app.route('/dids', methods=['GET'])
@token_required
def get_dids():
    page_items = DIDNumber.get_all_dids()
    return jsonify(page_items)


@app.route('/dids/<int:id>', methods=['GET'])
@token_required
def get_did_by_id(id):
    return_value = DIDNumber.get_did(id)
    return jsonify(return_value)

@app.route('/dids', methods=['POST'])
@token_required
def add_did():
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
def update_did(id):
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
def remove_did(id):
    DIDNumber.delete_did(id)
    response = Response("DID number deleted", status=200, mimetype='application/json')
    return response


if __name__ == "__main__":
    app.run(port=1234)
