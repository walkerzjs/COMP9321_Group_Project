from flask import Flask, render_template, request, Blueprint
import requests
import os
import json
import werkzeug.exceptions
from similarity_analysis import similarity_analysis
#from happiness_ranking_by_country.services import happiness_ranking_service

mod = Blueprint('two_country_comparison', __name__)

@mod.route('/view/two_country_comparison', methods=['GET', 'POST'])
def compare_countries():
    try:
        country1 = request.form['country1']
        country2 = request.form['country2']
        year = int(request.form['year'])
    except:
        country1 = "China"
        country2 = "India"
        year = 2015

    # get happiness & air pollution data for each
    #result = happiness_ranking_service.get_joint_and_sorted(str(year), 'Country', 1)
    #print(result)

    # get country cosine similarity
    country_dict = similarity_analysis.country_similarity_all(year, country1)
    similarity_val = country_dict[country2] * 100
    similarity_percent = "{0:.2f}%".format(similarity_val)

    # get coutry 2-letter code
    country1_url = 'https://restcountries.eu/rest/v2/name/' + country1
    country2_url = 'https://restcountries.eu/rest/v2/name/' + country2
    try:
        result = requests.get(country1_url)
        country_data = json.loads(result.content.decode())
        country1_code = country_data[0]['alpha2Code']
    except:
        country1_code = ""

    try:
        result = requests.get(country2_url)
        country_data = json.loads(result.content.decode())
        country2_code = country_data[0]['alpha2Code']
    except:
        country2_code = ""

    return render_template("two_country_comparison.html",
                           countries = country_dict, year=year,
                           country1_input = country1, country2_input = country2,
                           similarity_percent = similarity_percent,
                           country1_code = country1_code, country2_code = country2_code)
