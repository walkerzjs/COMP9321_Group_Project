from flask import Flask
import os
from correlation_analysis.view import correlation_analysis

here = os.path.dirname(os.path.abspath(__file__))
os.chdir(here)

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.register_blueprint(correlation_analysis.cor)

if __name__ == '__main__':
    app.run(port=1233)
