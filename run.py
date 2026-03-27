from app import create_app
from app.extensions import db
from app.models import Admin

app = create_app()

@app.cli.command("init-db")
def init_db():
    """Initialize the database and create the default admin account."""
    # app_context is required for db operations in Flask CLI commands
    with app.app_context():
        db.create_all()
        admin = Admin.query.filter_by(email="admin@portal.com").first()
        if not admin:
            admin = Admin(email="admin@portal.com", password="admin123")
            db.session.add(admin)
            db.session.commit()
            print("Default admin account created.")
            print("  Email:    admin@portal.com")
            print("  Password: admin123")
        else:
            print("Admin account already exists.")
        print("Database initialized successfully.")

if __name__ == '__main__':
    app.run(debug=True)
