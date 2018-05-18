from flask import Flask
import os
from data_publication_pm.api import pm_api
from data_curation.api import data_curation_api

here = os.path.dirname(os.path.abspath(__file__))
os.chdir(here)


app = Flask(__name__)
app.register_blueprint(pm_api.pm_app)
app.register_blueprint(data_curation_api.curation_app)

if __name__ == '__main__':
    app.run(port=5000)
