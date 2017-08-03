import re
import uuid

from flask import jsonify, current_app, request, make_response
from flask_restful import Resource, reqparse

import model
from Exception import *
from response import *


class PatientsEndpoint(Resource):
    RESULT_PER_PAGE = 10

    def get(self):
        request_id = uuid.uuid4()
        current_app.logger.debug("request received:{}".format(request_id))
        next_url = PatientsEndpoint.generate_next_url(request_id)
        results, has_next = model.Patient.get_patients(PatientsEndpoint.RESULT_PER_PAGE)
        next_url = next_url if has_next else ""
        return make_response(jsonify(
            {'data': [patient.to_json for patient in results], 'links': {'self': request.url, 'next': next_url}}), 200)

    def post(self):
        request_id = uuid.uuid4()
        current_app.logger.debug("request received:{}".format(request_id))
        parser = reqparse.RequestParser()
        parser.add_argument('data', type=dict, location='json')
        root = parser.parse_args()
        parser = reqparse.RequestParser()
        parser.add_argument('attributes', type=dict, location='data')
        args = parser.parse_args(root)
        if root.get('data') is None or args.get('attributes') is None:
            raise GeneralException(
                Error(req_id=request_id, status=400, title="Invalid request", detail="Invalid request"))
        try:
            new_patient = model.Patient.patient_parser(args.get('attributes'))
        except Exception as error:
            raise GeneralException(Error(req_id=request_id, status=400, title="Invalid request", detail=error.message,
                                         source=error.message))
        new_patient.save_to_db(request_id)
        current_app.logger.debug("patient record created:{!r}".format(new_patient))
        return make_response(jsonify(new_patient.to_json), 201)

    @classmethod
    def generate_next_url(cls, request_id):
        query_string = request.query_string
        page_regex = re.compile('(page=\d)')
        if query_string == '':
            next_url = request.url + '?page=2'
        elif not page_regex.search(query_string):
            raise GeneralException(
                Error(req_id=request_id, status=400, title="Bad request", detail="Page query not found"))
        else:
            current_page = request.args.get('page')
            try:
                next_url = request.base_url + '?page={}'.format(int(current_page) + 1)
            except (TypeError, ValueError):
                raise GeneralException(
                    Error(req_id=request_id, status=400, title="Bad request", detail="Invalid page query"))

        return next_url


class PatientEndpoint(Resource):
    def get(self, patient_id):
        result = model.Patient.query.filter_by(id=patient_id).first()
        request_id = uuid.uuid4()
        current_app.logger.debug("request received:{}".format(request_id))
        if result is None:
            raise GeneralException(
                Error(req_id=request_id, status=404, title="Not Found", detail="Patient record not found",
                      code=PATIENT_RECORD_NOT_FOUND))
        return jsonify(result.to_json)
