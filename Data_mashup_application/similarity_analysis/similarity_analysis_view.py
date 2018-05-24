from flask import Flask, render_template, request, Blueprint
import requests
import os
import json
from similarity_analysis import similarity_analysis
import werkzeug.exceptions as e
app = Flask(__name__)
here = os.path.dirname(os.path.abspath(__file__))
os.chdir(here)
mod = Blueprint('similarity_analysis_view', __name__)


# draw correlation graph from the combined data set
@mod.route('/view/similarity_analysis', methods=['GET', 'POST'])
def similarity_analysis_all():
    try:
        country = request.form['country']
#        feature2 = request.form['pm_happy_feature2']
        year = request.form['year']
    except e.BadRequestKeyError:
        print("##### ERROR#####")
#        feature1 = "PM2.5"
        country = "Australia"
        year = 2015

#    data = correlation_analysis_module.retrieve_joined_data(year)
#    data_json = {"data": data, "col1": feature1, "col2": feature2, "year": year}
#    url = "http://127.0.0.1:1233/api/correlation_analysis"
#    accept_tp = 'JSON'
#    result = requests.post(url, json=data_json,
#                           headers={"Content-Type": "application/json", "ACCEPT": accept_tp})
#    res_str = result.content.decode()
#    res_dict = json.loads(res_str)
    countryDict = similarity_analysis.country_similarity_all(year, country)
    print(countryDict)
    print("country: ",country)
    return render_template("similarity_analysis.html", countries = countryDict,
                           year=year, country_input = country)
