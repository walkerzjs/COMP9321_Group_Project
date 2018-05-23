from flask import Flask
from flask_cors import CORS
from application.api import happiness_ranking_api

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.register_blueprint(happiness_ranking_api.mod)
CORS(app)


if __name__ == '__main__':
    server_port = 7200
    app.run(port=server_port)
