from app import create_app, db
from app.seed import seed_demo_data

app = create_app()
with app.app_context():
    db.create_all()
    created = seed_demo_data()
    print(f"Demo data ready. New demo users created: {created}")
    print("Development-only password for all demo accounts: DemoPass123!")
