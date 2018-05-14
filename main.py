from flask import Flask
from flask_cors import CORS
from application.api import world_happiness_api

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.register_blueprint(world_happiness_api.mod)
CORS(app)


if __name__ == '__main__':
    server_port = 5000
    max_retries = 20
    for _ in range(max_retries):
        try:
            app.run(port=server_port)
        except OSError as e:
            if e.errno == 48:
                server_port += 150
            else:
                raise e
        else:
            break
    else:
        raise OSError(('Server cannot be started after trying '
                       '{} different ports.').format(max_retries))