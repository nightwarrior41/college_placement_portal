from flask import Flask
from config import Config
from app.extensions import db, login_manager
from datetime import datetime


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Register blueprints
    from app.routes.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.routes.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.routes.student import bp as student_bp
    app.register_blueprint(student_bp, url_prefix='/student')

    from app.routes.company import bp as company_bp
    app.register_blueprint(company_bp, url_prefix='/company')

    from app.routes.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Bug 5 Fix: inject current year into all templates
    @app.context_processor
    def inject_globals():
        return {'now_year': datetime.utcnow().year}

    return app
