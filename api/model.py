from dateutil import parser
from sqlalchemy.exc import IntegrityError

from Exception import *
from database import db
from response import *


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    birth_date = db.Column(db.Date)
    sex = db.Column(db.String(120))

    def __init__(self, email, first_name, last_name, birth_date, sex):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.sex = sex

    @property
    def to_json(self):
        return {
            'attributes': {
                'id': self.id,
                'email': self.email,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'birth_date': self.birth_date.strftime("%Y-%m-%d"),
                'sex': self.sex
            }

        }

    def __repr__(self):
        return '<User email: {!r}, first_name: {!r}, last_name: {!r}, birth_date: {!r}, sex: {!r}>'.format(self.email,
                                                                                                           self.first_name,
                                                                                                           self.last_name,
                                                                                                           self.birth_date,
                                                                                                           self.sex)

    @classmethod
    def patient_parser(cls, data):
        if 'email' not in data:
            raise ValueError('email is required')
        if 'first_name' not in data:
            raise ValueError('first_name is required')
        if 'last_name' not in data:
            raise ValueError('last_name is required')
        if 'birth_date' not in data:
            raise ValueError('birth_date is required')
        if 'sex' not in data:
            raise ValueError('sex is required')
        birth_date = parser.parse(data.get('birth_date'), yearfirst=True, dayfirst=False)

        return Patient(data.get('email'), data.get('first_name'), data.get('last_name'), birth_date.date(),
                       data.get('sex'))

    def save_to_db(self, request_id):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as e:
            raise GeneralException(Error(req_id=request_id, status=409, title="Conflict", detail="Duplicated email",
                                         code=PATIENT_RECORD_EMAIL_DUPLICATE, source=e.message))

    @classmethod
    def get_patients(cls, per_page):
        pagination = Patient.query.paginate(per_page=per_page, error_out=False)
        if pagination.has_next:
            return pagination.items, True
        elif pagination.items:
            return pagination.items, False
        else:
            raise GeneralException(
                Error(status=404, title="Not Found", detail="Page not found", code=PATIENT_RECORD_PAGE_NOT_FOUND))
