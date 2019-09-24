from flask import Blueprint, jsonify
from flask_restful import reqparse
from data_curation_correlation.modules import data_curation_modules
from werkzeug.exceptions import BadRequest

curation_app = Blueprint('curation_app', __name__)


# join the input pm2.5 data and world happiness report by country.
@curation_app.route('/api/join', methods=["POST"])
def join_data():
    parser = reqparse.RequestParser()
    try:
        parser.add_argument('pm', type=str)
        parser.add_argument('world_happiness', type=str)
        args = parser.parse_args()
        pm_json = args.get("pm")
        happy_json = args.get("world_happiness")
    except KeyError as e:
        return e
    combined_data = data_curation_modules.join_data("Country", pm_json, happy_json)
    return jsonify(combined_data), 200


# return the data for the mashup application to draw graphs
# also computes the Pearson correlation coefficient between the two input columns
@curation_app.route('/api/correlation_analysis', methods=["POST"])
def pm_happy_correlation():
    parser = reqparse.RequestParser()
    try:
        parser.add_argument('data', type=str)
        parser.add_argument('col1', type=str)
        parser.add_argument('col2', type=str)
        parser.add_argument('year', type=int)
        args = parser.parse_args()
        data = args.get("data")
        col1 = args.get("col1")
        col2 = args.get("col2")
        year = args.get("year")
    except BadRequest as e:
        return e
    except KeyError as ke:
        return ke
    data_obj = data_curation_modules.correlation_analysis(data, col1=col1, col2=col2, year=year)
    return jsonify(data_obj.__dict__)
