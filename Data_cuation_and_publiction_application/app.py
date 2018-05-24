from flask import Flask
from flask_cors import CORS
import os
#from data_publication_pm.api import pm_api
from data_publication_pollution import pm25_api
from data_curation_correlation.api import data_curation_api
from data_curation_similarity.api import data_curation_similarity
from data_publication_world_happiness.api import world_happiness_api


here = os.path.dirname(os.path.abspath(__file__))
os.chdir(here)


app = Flask(__name__)
#app.register_blueprint(pm_api.pm_app)
app.register_blueprint(data_curation_api.curation_app)
app.register_blueprint(pm25_api.mod)
app.register_blueprint(world_happiness_api.mod)
app.register_blueprint(data_curation_similarity.mod)
CORS(app)
if __name__ == '__main__':
    app.run(port=1234)
