from app import create_app
from app.seed import reset_demo_data

app = create_app()
with app.app_context():
    removed = reset_demo_data()
    print(f"Removed {removed} demo users and sample stories.")
