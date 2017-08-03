from flask_restful import Api

from patient_endpoints import PatientEndpoint, PatientsEndpoint

router = Api()

router.add_resource(PatientEndpoint, '/patients/<string:patient_id>')
router.add_resource(PatientsEndpoint, '/patients', '/patients/<string:page>')
