from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest, NotFound
from application.models import similarity_model
import numpy as np
import requests

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

    print(country1Data.json())
    # if country1Data:
    #     return country1Data.json(), 200
    # else:
    #     raise NotFound

    return 404


# def cos_sim(a, b):
#     # Takes 2 vectors a, b and returns the cosine similarity according to the definition of the dot product
#     dot_product = np.dot(a, b)
#     norm_a = np.linalg.norm(a)
#     norm_b = np.linalg.norm(b)
#
#     return dot_product / (norm_a * norm_b)
#
#
# # the counts we computed above
# sentence_m = np.array([1, 1, 1, 1, 0, 0, 0, 0, 0])
# sentence_h = np.array([0, 0, 1, 1, 1, 1, 0, 0, 0])
# sentence_w = np.array([0, 0, 0, 1, 0, 0, 1, 1, 1])
#
# # We should expect sentence_m and sentence_h to be more similar
# print(cos_sim(sentence_m, sentence_h))  # 0.5
# print(cos_sim(sentence_m, sentence_w))  # 0.25
