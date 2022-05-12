''' app factory '''

from flask import Flask
from .configs import Config, config_modes

db: SQLAlchemy = SQLAlchemy()
mail: Mail = Mail()

config_mode = environ.get("MODE") or "development"
config: Config = config_modes[config_mode]

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.refresh_view = "auth.login"

def load_all_models():
    pass
    # from .models import listings , address, auth, categories, filters, statics, stores, users


def create_app(alembic=False):
    app = Flask(__name__, subdomain_matching=True)

    config = config_modes[config_mode]

    app.config.from_object(config)
    config_modes[config_mode].init_app(app)

    bootstrap = Bootstrap4(app)
    
    
    db.init_app(app)
    
    
    # to log SQL queries 
    
    # import logging
    # logging.basicConfig()
    # logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    
    if alembic:
        # make the metadata object aware of all classes
        load_all_models()
    
    mail.init_app(app)

    wtforms_json.init()

    login_manager.init_app(app)

    from .cli import cli_bp as cli_blueprint

    app.register_blueprint(cli_blueprint)

    from werkzeug.middleware.proxy_fix import ProxyFix

    app.wsgi_app = ProxyFix(app.wsgi_app)

    # ########################################################
    # ############ User Types Distinct BluePrints ############
    # ########################################################

    # ############ Customer ############

    from .sites.main.api.v1 import customer_api as customer_api_v1

    app.register_blueprint(customer_api_v1)

    from .sites.main import main as web_customer_api

    app.register_blueprint(web_customer_api)

    # ############ Delivery ############

    from .sites.delivery_management import (
        delivery_management as delivery_management_blueprint,
    )

    app.register_blueprint(delivery_management_blueprint)

    # ############ Seller ############

    from .sites.seller.web import seller as seller_blueprint

    app.register_blueprint(seller_blueprint)

    from .sites.seller.web import public_seller as public_seller_blueprint

    app.register_blueprint(public_seller_blueprint)

    from .sites.management import management as management_blueprint

    app.register_blueprint(management_blueprint)

    from .sites.seller.api.v1 import seller_api as seller_api_blueprint_v1

    app.register_blueprint(seller_api_blueprint_v1)
    
    # ############ Management ############

    from .sites.management.api.v1 import management_api as management_api_blueprint_v1

    app.register_blueprint(management_api_blueprint_v1)
    
    # ############ Shared ############

    from .sites.shared.api.v1 import shared_api as shared_api_blueprint_v1

    app.register_blueprint(shared_api_blueprint_v1)

    # ########################################################

    from .auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    # ########################################################

    from .util_api import utils_endpoints as utils_blueprint

    app.register_blueprint(utils_blueprint)

    # from .api import api as api_blueprint
    # app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    app.debug = True

    # from .utils.handlers import not_found_handler

    # TODO TOREMOVE
    # if app.debug:
    #     app.config["TRAP_HTTP_EXCEPTIONS"] = True

    # app.register_error_handler(404, not_found_handler)

    return app
