from models import Base
from database import engine
import sqlalchemy
from sqlalchemy import text, create_engine

print("📦 Creating database tables...")
Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully!")
