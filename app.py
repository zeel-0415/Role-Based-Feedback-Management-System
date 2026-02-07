from flask import Flask
from config import Config
from extensions import db, login_manager
from models.user import User
from routes.auth_routes import auth
from routes.feedback_routes import feedback_bp
from routes.admin_routes import admin_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(auth, url_prefix="/")

app.register_blueprint(feedback_bp)
app.register_blueprint(admin_bp)

with app.app_context():
    db.create_all()

    # create admin
    from werkzeug.security import generate_password_hash
    if not User.query.filter_by(username="admin").first():
        admin = User(
            username="admin",
            password=generate_password_hash("admin123"),
            role="admin"
        )
        db.session.add(admin)
        db.session.commit()

app.run(debug=True)
