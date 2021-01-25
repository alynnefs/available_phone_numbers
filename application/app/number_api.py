from flask import jsonify, request, Response

from settings import app
from number_models import DIDNumber
from auth_models import User
from auth_api import token_required



@app.route('/')
@app.route('/dids', methods=['GET'])
@token_required
def get_dids():
    """
    This method gets paged users
    Returns:
        page_items (json): paged users
    """
    page_items = DIDNumber.get_all_dids()
    return jsonify(page_items)


@app.route('/dids/<int:id>', methods=['GET'])
@token_required
def get_did_by_id(id):
    """
    This method gets an user by id
    Returns:
        return_value (json): the user of the given id
    """
    return_value = DIDNumber.get_did(id)
    return jsonify(return_value)

@app.route('/dids', methods=['POST'])
@token_required
def add_did():
    """
    This method adds an user
    Returns:
        response (json): status 201 - if the user is correctly added
    """
    request_data = request.get_json()

    DIDNumber.add_did(
        request_data["value"],
        request_data["monthyPrice"],
        request_data["setupPrice"],
        request_data["currency"]
    )

    response = Response(
        "DID number added",
        201,
        mimetype='application/json'
    )
    return response


@app.route('/dids/<int:id>', methods=['PUT'])
@token_required
def update_did(id):
    """
    This method updates an user by id
    Returns:
        response (json): status 201 - if the user is correctly updated
    """
    request_data = request.get_json()
    DIDNumber.update_did(
        id,
        request_data["value"],
        request_data["monthyPrice"],
        request_data["setupPrice"],
        request_data["currency"]
    )
    response = Response(
        "DID number updated",
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/dids/<int:id>', methods=['DELETE'])
@token_required
def remove_did(id):
    """
    This method removes an user
    Returns:
        response (json): status 200 - if the user is correctly removed
    """
    DIDNumber.delete_did(id)
    response = Response(
        "DID number deleted",
        status=200,
        mimetype='application/json'
    )
    return response
