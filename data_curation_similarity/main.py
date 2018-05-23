from flask import Flask
from flask_cors import CORS
from data_curation_similarity.application.api import data_curation_similarity

app = Flask(__name__)
app.debug = True
app.register_blueprint(data_curation_similarity.mod)
CORS(app)


if __name__ == '__main__':
    server_port = 5002

    app.run(port=server_port)
