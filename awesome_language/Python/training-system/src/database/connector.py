from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

class TrainingDataORM(Base):
    __tablename__ = 'training_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    instruction = Column(Text, nullable=False)
    input = Column(Text, default="")
    output = Column(Text, nullable=False)
    source = Column(String(50))
    status = Column(String(20), default="pending")

class DBManager:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(bind=self.engine)
    
    def init_db(self):
        Base.metadata.create_all(self.engine)
