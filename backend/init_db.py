from database import engine
from model import Base
from sqlalchemy.exc import OperationalError
from sqlalchemy import inspect, text
import time
import crud, models, schemas
from database import SessionLocal, engine


def init_db(retries=10, delay=3):

    Base.metadata.create_all(bind=engine)
    inspector = inspect(engine)
    if inspector.has_table("users"):
        user_columns = {col["name"] for col in inspector.get_columns("users")}
        if "year" not in user_columns:
            with engine.begin() as conn:
                conn.execute(text("ALTER TABLE users ADD COLUMN year VARCHAR(20) NULL"))
            print("✅ Added users.year column")
    print("✅ Database initialized and tables created.")
            

if __name__ == "__main__":
    init_db()
