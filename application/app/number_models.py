from settings import app, db
from flask import abort, jsonify, make_response, request

from paginator import paginate


class DIDNumber(db.Model):
    """
    This class models the DID numbers
    """
    __tablename__ = 'did_number'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String(17))
    monthyPrice = db.Column(db.Numeric(scale=2, precision=8, decimal_return_scale=2))
    setupPrice = db.Column(db.Numeric(scale=2, precision=8, decimal_return_scale=2))
    currency = db.Column(db.String(5))

    def __init__(self, value, monthyPrice, setupPrice, currency):
        """
        This method verifies negative numbers and assigns given values.
        If one of the prices ​​is negative, abort the request.
        """
        if monthyPrice < 0 or setupPrice < 0:
            abort(make_response(jsonify(message="negative value"), 400))

        self.value = str(value)
        self.monthyPrice = monthyPrice
        self.setupPrice = setupPrice
        self.currency = str(currency)

    def __repr__(self):
        """
        This method returns the current id
        """
        return f'<id {self.id}>'

    def json(self):
        """
        This method returns a json with the DID's attributes
        """
        return {
            'id': self.id,
            'value': str(self.value),
            'monthyPrice': str(self.monthyPrice),
            'setupPrice': str(self.setupPrice),
            'currency': str(self.currency)
        }

    def add_did(_value, _monthyPrice, _setupPrice, _currency):
        """
        This method adds a DID number
        """
        new_did = DIDNumber(
            value = _value,
            monthyPrice = _monthyPrice,
            setupPrice = _setupPrice,
            currency = _currency
        )
        db.session.add(new_did)
        db.session.commit()

    def get_all_dids():
        """
        This method gets all DID numbers
        """
        try:
            page = int(request.args.get('page', 1))
            per_page = int(request.args.get('per_page', 50))
        except Exception as e:
            return jsonify({'exception': e})

        response = paginate(
            DIDNumber.query.order_by(DIDNumber.id),
            page=page,
            per_page=per_page
        )
        items = response['items']

        return items

    def get_did(_id):
        """
        This method gets a DID number by id
        """
        return [DIDNumber.json(DIDNumber.query.filter_by(id=_id).first())]

    def update_did(_id, _value, _monthyPrice, _setupPrice, _currency):
        """
        This method updates a DID number
        """
        did_to_update = DIDNumber.query.filter_by(id=_id).first()
        did_to_update.value = _value
        did_to_update.monthyPrice = _monthyPrice
        did_to_update.setupPrice = _setupPrice
        did_to_update.currency = _currency
        db.session.commit()

    def delete_did(_id):
        """
        This method removes a DID number
        """
        DIDNumber.query.filter_by(id=_id).delete()
        db.session.commit()
