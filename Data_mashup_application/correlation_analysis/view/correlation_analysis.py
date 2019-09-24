from flask import Flask, render_template, request, Blueprint
import requests
import os
import json
from correlation_analysis.modules import correlation_analysis_module
import werkzeug.exceptions as e
#app = Flask(__name__)
#here = os.path.dirname(os.path.abspath(__file__))
#os.chdir(here)
cor = Blueprint('correlation_analysis', __name__)


# draw correlation graph from the combined data set
@cor.route('/view/correlation_analysis', methods=['GET', 'POST'])
def analyse_pm_happy():
    try:
        feature1 = request.form['pm_happy_feature1']
        feature2 = request.form['pm_happy_feature2']
        year = request.form['year']
    except e.BadRequestKeyError:
        feature1 = "PM2.5"
        feature2 = "Happiness Score"
        year = 2015

    data = correlation_analysis_module.retrieve_joined_data(year)
    data_json = {"data": data, "col1": feature1, "col2": feature2, "year": year}
    url = "http://127.0.0.1:1234/api/correlation_analysis"
    accept_tp = 'JSON'
    result = requests.post(url, json=data_json,
                           headers={"Content-Type": "application/json", "ACCEPT": accept_tp})
    res_str = result.content.decode()
    res_dict = json.loads(res_str)
    return render_template("correlation_analysis_new.html", data=res_dict['data_list'], cols=res_dict['cols'],
                           pr=res_dict['pr'], p=res_dict['p_value'], features=res_dict['features'],
                           year=year)

@cor.route('/view/correlation_analysis_new_ajax', methods=['GET'])
def analyse_pm_happy_new():

    return render_template("correlation_analysis_new_ajax.html")
