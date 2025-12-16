from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

db_url = "mysql+mysqlconnector://root:12345678@localhost:3306/telusko1"
engine = create_engine(db_url, echo=True)
session = sessionmaker(autocommit = False , autoflush = False, bind =engine)


