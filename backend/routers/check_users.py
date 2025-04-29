import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import SessionLocal
from app.models import User


db = SessionLocal()
users = db.query(User).all()

# Print user details
print("User details:")

for user in users:
    print(f"UserName: {user.username}, Email: {user.email}")
