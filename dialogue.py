def create_app():
    from flask import Flask, make_response, jsonify
    from api import patient_api
    from api.Exception import GeneralException
    from api.database import db
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:dialogue_db@172.17.0.1:3306/core'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)
    app.register_blueprint(patient_api)

    @app.errorhandler(GeneralException)
    def handle_invalid_usage(error):
        return make_response(jsonify(
            {'errors': [error.get_error.to_json]}), error.get_error.status)

    @app.errorhandler(404)
    def handle_invalid_usage(error):
        from api.response import Error
        return make_response(jsonify(
            {'errors': [Error.create_not_found_exception().to_json]}), 404)

    with app.app_context():
        db.create_all()

    return app


application = create_app()

if __name__ == '__main__':
    application.run(host="0.0.0.0", debug=True, port=8080)
