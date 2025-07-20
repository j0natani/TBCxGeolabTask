from ext import app, db 
from models import Product, User

with app.app_context():
    print("Dropping all tables...")
    db.drop_all()
    print("Creating all tables...")
    db.create_all()
    print("Done.")

    admin = User(username="Admin",password="adminpass1",role="Admin")
    db.session.add(admin)
    db.session.commit()