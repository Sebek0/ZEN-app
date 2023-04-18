import os

from sqlalchemy import (Column, Integer, String, Table, create_engine, MetaData)
from dotenv import load_dotenv
from databases import Database
from datetime import datetime as dt
from pytz import timezone as tz

load_dotenv()
# Database url if none is passed the default one is used
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://zenapp:zenapp@localhost/zenapp_dev")

# SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Databases query builder

database = Database(DATABASE_URL)
