from flask import jsonify, request, Response

from settings import app
from app_models import DIDNumber


@app.route('/')
@app.route('/dids', methods=['GET'])
def get_dids():
    return jsonify({
        'DID Numbers': DIDNumber.get_all_dids()
    })

@app.route('/dids/<int:id>', methods=['GET'])
def get_did_by_id(id):
    return_value = DIDNumber.get_did(id)
    return jsonify(return_value)

@app.route('/dids', methods=['POST'])
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
def remove_did(id):
    DIDNumber.delete_did(id)
    response = Response("DID number deleted", status=200, mimetype='application/json')
    return response


if __name__ == "__main__":
    app.run()
