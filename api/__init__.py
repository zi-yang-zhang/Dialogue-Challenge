from flask_restful import Api

from patient import Patient, Patients

router = Api()

router.add_resource(Patient, '/patients', '/patients/<string:patient_id>')
router.add_resource(Patients, '/patients')
