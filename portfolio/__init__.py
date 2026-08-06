import os

from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect

from config import config_by_name


csrf = CSRFProtect()


def create_app(config_name=None):
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    selected_config = config_name or os.getenv("FLASK_ENV", "development")
    config_class = config_by_name.get(selected_config, config_by_name["development"])
    app.config.from_object(config_class)

    if hasattr(config_class, "init_app"):
        config_class.init_app(app)

    csrf.init_app(app)

    from portfolio.routes.main import main_bp
    from portfolio.routes.projects import projects_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(projects_bp)

    @app.errorhandler(404)
    def not_found(error):
        return render_template("404.html"), 404

    return app