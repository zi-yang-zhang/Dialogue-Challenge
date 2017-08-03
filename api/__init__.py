from flask import Blueprint
from flask_restful import Api

from patient_endpoints import PatientEndpoint, PatientsEndpoint

patient_api = Blueprint("patient_api", __name__)

router = Api(patient_api)

router.add_resource(PatientEndpoint, '/patients/<string:patient_id>')
router.add_resource(PatientsEndpoint, '/patients', '/patients/<string:page>')
