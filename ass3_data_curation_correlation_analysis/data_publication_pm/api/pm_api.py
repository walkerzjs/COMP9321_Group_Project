from flask import Blueprint, jsonify
from data_publication_pm.modules import pm_module

pm_app = Blueprint('pm_app', __name__)

# get the pm2.5 data
# this is not a real data publication api because it loads data from local file without downloading it at the first time.
@pm_app.route('/api/pm/<year>', methods=["GET"])
def get_pm_data(year):
    pm_json = pm_module.get_pm_data(year)
    return jsonify(pm_json), 200
