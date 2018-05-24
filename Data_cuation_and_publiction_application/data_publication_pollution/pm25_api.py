from flask import Flask, request, jsonify,Blueprint
from werkzeug.exceptions import BadRequest, NotFound
from data_publication_pollution import pm25_model

mod = Blueprint('pm25', __name__)

@mod.route('/api/air_pollution', methods=['GET'])
def get_all_data():
    result = pm25_model.get_sorted_collection()
    if result is not None:
        return jsonify(collection=result), 200
    else:
        raise NotFound


@mod.route('/api/air_pollution/<int:year>', methods=['GET'])
def get_data_by_year(year):
    result = pm25_model.get_entry_by_year(year)
    if result is not None:
        return jsonify(result), 200
    else:
        raise NotFound


@mod.route('/api/air_pollution/<country>', methods=['GET'])
def get_data_by_country(country):
    result = pm25_model.get_entry_by_country(country)
    if result is not None:
        return jsonify(result), 200
    else:
        raise NotFound


@mod.route('/api/air_pollution/filter', methods=['GET'])
def get_data_by_filter():
    if 'year' not in request.args or 'country' not in request.args:
        raise BadRequest
    try:
        year = int(request.args['year'])
    except ValueError:
        raise BadRequest
    country = request.args['country']
    result = pm25_model.get_entry_by_filter(year, country)
    if result is not None:
        return jsonify(result), 200
    else:
        raise NotFound



