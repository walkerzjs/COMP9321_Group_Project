from flask import Flask
from flask_cors import CORS
from application.api import happiness_ranking_api
from application.controllers import happiness_ranking_controller


# If the template folder setting here doesn't work outside of PyCharm,
# then it needs to be set for each Blueprint.
# Test this setting on both Mac and Windows before pushing to Github.
app = Flask(__name__, static_folder='application/static',
            template_folder='application/templates')
app.config['JSON_SORT_KEYS'] = False
app.register_blueprint(happiness_ranking_api.mod)
app.register_blueprint(happiness_ranking_controller.mod)
CORS(app)


if __name__ == '__main__':
    server_port = 7200
    app.run(port=server_port)
