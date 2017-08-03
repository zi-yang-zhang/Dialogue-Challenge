from flask import Flask

from api import router
from api.database import db

app = Flask(__name__)
db.init_app(app)
router.init_app(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=8080)
