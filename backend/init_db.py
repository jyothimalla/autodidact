from database import engine
from model import Base
from sqlalchemy.exc import OperationalError
import time
import crud, models, schemas
from database import SessionLocal, engine


def init_db(retries=10, delay=3):

    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized and tables created.")
            

if __name__ == "__main__":
    init_db()
