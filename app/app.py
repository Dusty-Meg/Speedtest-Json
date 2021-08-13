from flask_restful import Api
from flask import Flask

from Routes import initialize_routes

app = Flask(__name__)
api = Api(app)

initialize_routes(api)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
