from flask import Flask
from flask_cors import CORS
from application.api import world_happiness_api

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.register_blueprint(world_happiness_api.mod)
CORS(app)


if __name__ == '__main__':
    server_port = 5000
    app.run(port=server_port)
