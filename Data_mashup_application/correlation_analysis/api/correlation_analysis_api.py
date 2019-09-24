from flask import Flask, render_template, request, Blueprint,jsonify
import requests
import os
import json
from correlation_analysis.modules import correlation_analysis_module
import werkzeug.exceptions as e

mod = Blueprint('correlation_analysis_api', __name__)


# draw correlation graph from the combined data set
@mod.route('/api/correlation_analysis', methods=['GET'])
def analyse_pm_happy_api():
    try:
#        feature1 = request.form['pm_happy_feature1']
#        feature2 = request.form['pm_happy_feature2']
#        year = request.form['year']
        year = request.args['year']
        feature1 = request.args['pm_happy_feature1']
        feature2 = request.args['pm_happy_feature2']
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
    return jsonify(data=res_dict['data_list'], cols=res_dict['cols'],
                           pr=res_dict['pr'], p=res_dict['p_value'], features=res_dict['features'],
                           year=year)
