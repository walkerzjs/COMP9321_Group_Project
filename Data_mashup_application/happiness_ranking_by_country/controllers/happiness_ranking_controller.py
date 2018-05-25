from flask import Blueprint, render_template


mod = Blueprint('happiness_ranking_controller', __name__)


@mod.route('/', methods=['GET'])
def show_happiness_ranking():
    return render_template('happiness_ranking.html')
