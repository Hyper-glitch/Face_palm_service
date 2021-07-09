import logging
import sys
from argparse import ArgumentParser
from flask import Flask
from flask_migrate import Migrate
from auth import auth as auth_blueprint
from database import db
from main import main as main_blueprint


def setup_logging(log_level=logging.DEBUG):
    # file handler
    file_handler = logging.FileHandler('face_palm_service.log')
    log_format = logging.Formatter("[%(asctime)s] - %(levelname)s - %(module)s : %(message)s")
    file_handler.setFormatter(log_format)
    file_handler.setLevel(log_level)

    # werkzeug handler
    werkzeug_handler = logging.FileHandler('flask_werkzeug.log')
    werkzeug_handler.setFormatter(log_format)

    # stdout handler
    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    stdout_handler.setLevel(log_level)
    stdout_handler.setFormatter(log_format)

    # add handlers
    werkzeug_log = logging.getLogger('werkzeug')
    werkzeug_log.setLevel(log_level)

    main_logger = logging.getLogger('main')
    main_logger.setLevel(log_level)

    auth_logger = logging.getLogger('auth')
    auth_logger.setLevel(log_level)

    camera_logger = logging.getLogger('camera')
    camera_logger.setLevel(log_level)

    main_logger.addHandler(file_handler)
    main_logger.addHandler(stdout_handler)

    auth_logger.addHandler(file_handler)
    auth_logger.addHandler(stdout_handler)

    camera_logger.addHandler(file_handler)
    camera_logger.addHandler(stdout_handler)

    werkzeug_log.addHandler(werkzeug_handler)


def parse_args():
    parser = ArgumentParser(description="This FacePalmService application allows you to SIGN UP and SIGN IN to the "
                                        "system just with your Face and Username")
    parser.version = "1.0"
    parser.add_argument("-V", "--version", action="version")
    parser.add_argument('-H', '--host',
                        help='host ip',
                        required=True,
                        default='localhost')
    parser.add_argument('-p', '--port',
                        help='port of the web server',
                        required=True,
                        default='5000')
    parser.add_argument('-u', '--user',
                        help='user name',
                        default='root')

    cli_args = parser.parse_args()
    return cli_args


def create_app():
    setup_logging()
    args = parse_args()
    port = args.port
    host = args.host

    app = Flask(__name__)
    app.config['SECRET_KEY'] = '@w2rtpv^_1tewn'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['ENV'] = 'development'
    app.config['DEBUG'] = True
    app.config['TESTING'] = True

    db.init_app(app)
    migrate = Migrate(app, db)

    # blueprint for auth routes in our app
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    app.register_blueprint(main_blueprint)

    app.run(debug=True, port=port, host=host)


if __name__ == '__main__':
    create_app()
