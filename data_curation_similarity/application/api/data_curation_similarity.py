from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest, NotFound
from application.models import similarity_model
import numpy as np
import requests
from scipy import spatial

mod = Blueprint('data_curation_similarity', __name__)

url = "http://127.0.0.1:5000/"
worldHappinessRoute = "api/world_happiness/"


# Computes the similarity of two countries based on world happiness report
@mod.route('/api/similarity/', methods=['GET'])
def compute_similarity():
    country1 = request.args.get('country1')
    country2 = request.args.get('country2')

    country1Data = requests.get(url + worldHappinessRoute + country1)
    country2Data = requests.get(url + worldHappinessRoute + country2)

    country1JSON = country1Data.json()
    country2JSON = country2Data.json()

    country1Array = [country1JSON['Happiness Rank']['2015'],
                     country1JSON['Happiness Score']['2015'],
                     country1JSON['Economy GDP per Capita']['2015'],
                     country1JSON['Family']['2015'],
                     country1JSON['Health Life Expectancy']['2015'],
                     country1JSON['Freedom']['2015'],
                     country1JSON['Trust Government Corruption']['2015'],
                     country1JSON['Generosity']['2015'],
                     country1JSON['Dystopia Residual']['2015'],
                     ]

    country2Array = [country2JSON['Happiness Rank']['2015'],
                     country2JSON['Happiness Score']['2015'],
                     country2JSON['Economy GDP per Capita']['2015'],
                     country2JSON['Family']['2015'],
                     country2JSON['Health Life Expectancy']['2015'],
                     country2JSON['Freedom']['2015'],
                     country2JSON['Trust Government Corruption']['2015'],
                     country2JSON['Generosity']['2015'],
                     country2JSON['Dystopia Residual']['2015'],
                     ]

    result = 1 - spatial.distance.cosine(country1Array, country2Array)

    if country1Data and country2Data:
        return jsonify(Country1=country1Array, Country2=country2Array, Similarity=result), 200
    else:
        raise NotFound
