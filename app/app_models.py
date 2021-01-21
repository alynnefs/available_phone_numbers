from settings import app, db


class DIDNumber(db.Model):
    __tablename__ = 'didnumber'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String(17))
    monthyPrice = db.Column(db.Numeric(scale=2, precision=8, decimal_return_scale=2))
    setupPrice = db.Column(db.Numeric(scale=2, precision=8, decimal_return_scale=2))
    currency = db.Column(db.String(5))

    def __init__(self, value, monthyPrice, setupPrice, currency):
        self.value = value
        self.monthyPrice = monthyPrice
        self.setupPrice = setupPrice
        self.currency = currency

    def __repr__(self):
        return f'<id {self.id}>'

    def json(self):
        return {
            'id': self.id,
            'value': self.value,
            'monthyPrice': str(self.monthyPrice),
            'setupPrice': str(self.setupPrice),
            'currency': self.currency
        }

    def add_did(_value, _monthyPrice, _setupPrice, _currency):
        new_did = DIDNumber(
            value = _value,
            monthyPrice = _monthyPrice,
            setupPrice = _setupPrice,
            currency = _currency
        )
        db.session.add(new_did)
        db.session.commit()

    def get_all_dids():
        return [DIDNumber.json(did) for did in DIDNumber.query.all()]

    def get_did(_id):
        return [DIDNumber.json(DIDNumber.query.filter_by(id=_id).first())]

    def update_did(_id, _value, _monthyPrice, _setupPrice, _currency):
        did_to_update = DIDNumber.query.filter_by(id=_id).first()
        did_to_update.value = _value
        did_to_update.monthyPrice = _monthyPrice
        did_to_update.setupPrice = _setupPrice
        did_to_update.currency = _currency
        db.session.commit()

    def delete_did(_id):
        DIDNumber.query.filter_by(id=_id).delete()
        db.session.commit()
