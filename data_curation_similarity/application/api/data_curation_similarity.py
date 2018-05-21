from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest, NotFound
import numpy as np
import requests
from scipy import spatial

mod = Blueprint('data_curation_similarity', __name__)

url = "http://127.0.0.1:5000/"
worldHappinessRouteSingle = "api/world_happiness/"
worldHappinessRouteAll = "api/world_happiness/"


# Computes the similarity of two countries based on world happiness report
@mod.route('/api/similarity/', methods=['GET'])
def compute_similarity():
    country1 = request.args.get('country1')
    country2 = request.args.get('country2')
    year = request.args.get('year')

    country1Data = requests.get(url + worldHappinessRouteSingle + country1)
    country2Data = requests.get(url + worldHappinessRouteSingle + country2)

    country1JSON = country1Data.json()
    country2JSON = country2Data.json()

    country1Array = [country1JSON['Happiness Rank'][year],
                     country1JSON['Happiness Score'][year],
                     country1JSON['Economy GDP per Capita'][year],
                     country1JSON['Family']['2015'],
                     country1JSON['Health Life Expectancy'][year],
                     country1JSON['Freedom']['2015'],
                     country1JSON['Trust Government Corruption'][year],
                     country1JSON['Generosity'][year],
                     country1JSON['Dystopia Residual'][year],
                     ]

    country2Array = [country2JSON['Happiness Rank'][year],
                     country2JSON['Happiness Score'][year],
                     country2JSON['Economy GDP per Capita'][year],
                     country2JSON['Family'][year],
                     country2JSON['Health Life Expectancy'][year],
                     country2JSON['Freedom'][year],
                     country2JSON['Trust Government Corruption'][year],
                     country2JSON['Generosity'][year],
                     country2JSON['Dystopia Residual'][year],
                     ]

    result = 1 - spatial.distance.cosine(country1Array, country2Array)

    if country1Data and country2Data:
        return jsonify(Country1=country1Array, Country2=country2Array, Similarity=result), 200
    else:
        raise NotFound


# Computes the similarity of one country compared to every other country based on world happiness report
@mod.route('/api/similarity/all', methods=['GET'])
def compute_similarity_all():
    country1 = request.args.get('country1')
    year = request.args.get('year')

    country1Data = requests.get(url + worldHappinessRouteSingle + country1)
    allCountryData = requests.get(url + worldHappinessRouteAll + year)

    country1JSON = country1Data.json()
    allCountryJSON = allCountryData.json()

    country1Array = [country1JSON['Happiness Rank'][year],
                     country1JSON['Happiness Score'][year],
                     country1JSON['Economy GDP per Capita'][year],
                     country1JSON['Family']['2015'],
                     country1JSON['Health Life Expectancy'][year],
                     country1JSON['Freedom']['2015'],
                     country1JSON['Trust Government Corruption'][year],
                     country1JSON['Generosity'][year],
                     country1JSON['Dystopia Residual'][year],
                     ]

    countryDict = {}

    for country in allCountryJSON['data']['Happiness Rank'].keys():
        countryArray = list()
        countryArray.append(allCountryJSON['data']['Happiness Rank'][country])
        countryArray.append(allCountryJSON['data']['Happiness Score'][country])
        countryArray.append(allCountryJSON['data']['Economy GDP per Capita'][country])
        countryArray.append(allCountryJSON['data']['Family'][country])
        countryArray.append(allCountryJSON['data']['Health Life Expectancy'][country])
        countryArray.append(allCountryJSON['data']['Freedom'][country])
        countryArray.append(allCountryJSON['data']['Trust Government Corruption'][country])
        countryArray.append(allCountryJSON['data']['Generosity'][country])
        countryArray.append(allCountryJSON['data']['Dystopia Residual'][country])

        result = 1 - spatial.distance.cosine(country1Array, countryArray)

        countryDict[country] = result

    if country1Data and countryDict:
        return jsonify(Similarity=countryDict), 200
    else:
        raise NotFound

