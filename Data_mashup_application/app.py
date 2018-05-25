from flask import Flask,render_template
import os
from flask_cors import CORS
from correlation_analysis.view import correlation_analysis
from similarity_analysis import similarity_analysis_view
from similarity_analysis import similarity_analysis
from happiness_ranking_by_country.api import happiness_ranking_api
from happiness_ranking_by_country.controllers import happiness_ranking_controller

here = os.path.dirname(os.path.abspath(__file__))
os.chdir(here)

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.register_blueprint(correlation_analysis.cor)
app.register_blueprint(similarity_analysis.mod)
app.register_blueprint(similarity_analysis_view.mod)
app.register_blueprint(happiness_ranking_api.mod)
app.register_blueprint(happiness_ranking_controller.mod)

CORS(app)

#
#@app.route('/', methods=['GET', 'POST'])
#def homepage():
#    return render_template("base.html")

if __name__ == '__main__':
    app.run(port=1233)
