from flask import Blueprint, request
from werkzeug.exceptions import BadRequest, NotFound
from happiness_ranking_by_country.services import happiness_ranking_service


mod = Blueprint('happiness_ranking_api', __name__)


# requests must supply 'year', 'sort_by' and 'ascending' in query string
# year must be in ['2015', '2016']
# sort_by must be a column name string in the joint DataFrame
# ascending must be in ['0', '1'], representing False and True
@mod.route('/api/happiness_ranking', methods=['GET'])
def get_joint_and_sorted_by_year():
    if 'year' not in request.args or 'sort_by' not in request.args \
            or 'ascending' not in request.args:
        raise BadRequest
    year = request.args['year']
    if not year.isnumeric() or len(year) != 4:
        raise BadRequest
    sort_by = request.args['sort_by']
    ascending = request.args['ascending']
    if not ascending.isnumeric() or int(ascending) not in [0, 1]:
        raise BadRequest
    result = happiness_ranking_service.get_joint_and_sorted(
        year, sort_by, int(ascending))
    if result == False:
        raise BadRequest
    elif result == None:
        raise NotFound
    else:
        return result, 200, {'Content-Type': 'application/json'}
