import os

from flask import Flask
from flask_cors import CORS, cross_origin

def create_app():
    app = Flask(__name__)
    CORS(app)
    # app.config['CORS_HEADERS'] = 'Content-Type'

    app.config.from_mapping(
        SECRET_KEY='mikey',
        DATABASE_HOST=os.environ.get('FLASK_DATABASE_HOST'),
        DATABASE_PASSWORD=os.environ.get('FLASK_DATABASE_PASSWORD'),
        DATABASE_USER=os.environ.get('FLASK_DATABASE_USER'),
        DATABASE=os.environ.get('FLASK_DATABASE'),
    )

    from . import db

    db.init_app(app)

    from . import graphs

    app.register_blueprint(graphs.bp)
    
    @app.route("/hola")
    def hola():
        return "<p>hola</p>"

    return app