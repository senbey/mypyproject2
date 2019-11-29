from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
	"""Initialize the core application."""
	app = Flask(__name__, instance_relative_config=False)
	#app.config.from_object('config.Config')
	app.config.from_pyfile('../config_file.cfg')
	#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
	# Initialize Plugins
	db.init_app(app)
	#r.init_app(app)

	with app.app_context():
	# Include our Routes
		from . import routes

		# Register Blueprints
		#app.register_blueprint(auth.auth_bp)
		#app.register_blueprint(admin.admin_bp)

		return app