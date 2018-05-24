from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest, NotFound
from data_publication_world_happiness.models import world_happiness_model

mod = Blueprint('world_happiness', __name__)


# Returns all 3 years data of all countries.
@mod.route('/api/world_happiness', methods=['GET'])
def get_all_data():
    result = world_happiness_model.get_collection()
    if result:
        return jsonify(collection=result), 200
    else:
        raise NotFound


# Returns 1 year data of all countries.
# 2015 <= year <= 2017
@mod.route('/api/world_happiness/<int:year>', methods=['GET'])
def get_data_by_year(year):
    result = world_happiness_model.get_entry_by_year(year)
    if result:
        return jsonify(result), 200
    else:
        raise NotFound


# Returns all 3 years data of one country.
@mod.route('/api/world_happiness/<country>', methods=['GET'])
def get_data_by_country(country):
    result = world_happiness_model.get_entries_by_country(country)
    if result:
        return jsonify(result), 200
    else:
        raise NotFound


# Returns 1 year data of one country.
# Request must provide filter (year and country) in URL query string
@mod.route('/api/world_happiness/filter', methods=['GET'])
def get_data_by_filter():
    if 'year' not in request.args or 'country' not in request.args:
        raise BadRequest
    year = int(request.args['year'])
    country = request.args['country']
    result = world_happiness_model.get_entry_by_filter(year, country)
    if result:
        return jsonify(result), 200
    else:
        raise NotFound


# Delete all data.
# Not implemented in app GUI. Accessible through browser's REST API plugin.
@mod.route('/api/world_happiness', methods=['DELETE'])
def delete_all_data():
    result = world_happiness_model.delete_collection()
    if result:
        return '', 200
    else:
        raise NotFound
