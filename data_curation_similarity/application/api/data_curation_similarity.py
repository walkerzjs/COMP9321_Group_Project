from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest, NotFound
import numpy as np
import requests
from scipy import spatial

mod = Blueprint('data_curation_similarity', __name__)

urlWorldHappiness = "http://127.0.0.1:5000/"
urlPollution = "http://127.0.0.1:5001/"
worldHappinessRouteSingle = "api/world_happiness/"
worldHappinessRouteAll = "api/world_happiness/"
pollutionRouteSingle = "api/air_pollution/filter"
pollutionRouteAll = "api/air_pollution/"


# Computes the similarity of two countries based on world happiness report
@mod.route('/api/similarity/', methods=['GET'])
def compute_similarity():
    country1 = request.args.get('country1')
    country2 = request.args.get('country2')
    year = request.args.get('year')

    country1Data = requests.get(urlWorldHappiness + worldHappinessRouteSingle + country1)
    country2Data = requests.get(urlWorldHappiness + worldHappinessRouteSingle + country2)

    country1Pollution = requests.get(urlPollution + pollutionRouteSingle + "?country=" + country1 + "&year=" + year)
    country2Pollution = requests.get(urlPollution + pollutionRouteSingle + "?country=" + country2 + "&year=" + year)

    country1JSON = country1Data.json()
    country1JSONPollution = country1Pollution.json()
    country2JSON = country2Data.json()
    country2JSONPollution = country2Pollution.json()

    print(country1JSON['Happiness Rank'][year])
    print(country1JSONPollution[year])
    country1Array = [country1JSON['Happiness Rank'][year],
                     country1JSON['Happiness Score'][year],
                     country1JSON['Economy GDP per Capita'][year],
                     country1JSON['Family']['2015'],
                     country1JSON['Health Life Expectancy'][year],
                     country1JSON['Freedom']['2015'],
                     country1JSON['Trust Government Corruption'][year],
                     country1JSON['Generosity'][year],
                     country1JSON['Dystopia Residual'][year],
                     country1JSONPollution[year]
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
                     country2JSONPollution[year]
                     ]

    result = 1 - spatial.distance.cosine(country1Array, country2Array)

    if country1Data and country2Data:
        return jsonify(Country1=country1Array, Country2=country2Array, Similarity=result), 200
    else:
        raise NotFound


# Computes the similarity of one country compared to every other country based on world happiness report
@mod.route('/api/similarity/all', methods=['GET'])
def compute_similarity_all():
    country1 = request.args.get('country')
    year = request.args.get('year')

    country1Data = requests.get(urlWorldHappiness + worldHappinessRouteSingle + country1)
    country1Pollution = requests.get(urlPollution + pollutionRouteSingle + "?country=" + country1 + "&year=" + year)

    allCountryData = requests.get(urlWorldHappiness + worldHappinessRouteAll + year)
    allCountryPollutionData = requests.get(urlPollution + pollutionRouteAll + year)

    country1JSON = country1Data.json()
    country1JSONPollution = country1Pollution.json()

    allCountryJSON = allCountryData.json()
    allCountryJSONPollution = allCountryPollutionData.json()

    country1Array = [country1JSON['Happiness Rank'][year],
                     country1JSON['Happiness Score'][year],
                     country1JSON['Economy GDP per Capita'][year],
                     country1JSON['Family']['2015'],
                     country1JSON['Health Life Expectancy'][year],
                     country1JSON['Freedom']['2015'],
                     country1JSON['Trust Government Corruption'][year],
                     country1JSON['Generosity'][year],
                     country1JSON['Dystopia Residual'][year],
                     country1JSONPollution[year]
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
        # JSON pollution is missing for these countries:
        # Venezuela, Taiwan, Slovakia
        # South Korea, Russia, North Cyprus, Kosovo, Hong Kongm Kyrgyzstanm,
        # Somaliland region, Macedonia, Laos, Palestinian, Territories, Iran, Zimbabwe, Congo(Kinshasa), Egypt
        # Yemen ,Congo(Brazzaville) ,Ivory Coast ,Syria
        # So set pollution to a default value of 0
        if country in allCountryJSONPollution:
            countryArray.append(allCountryJSONPollution[country])
        else:
            countryArray.append(0)

        result = 1 - spatial.distance.cosine(country1Array, countryArray)

        countryDict[country] = result

    if country1Data and countryDict:
        return jsonify(Similarity=countryDict), 200
    else:
        raise NotFound

