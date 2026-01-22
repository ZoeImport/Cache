from src.database.connector import DBManager, TrainingDataORM
from src.schema.data_types import TrainingSample

class Repository:
    def __init__(self, db: DBManager):
        self.db = db

    def get_pending(self, limit=10):
        session = self.db.SessionLocal()
        try:
            records = session.query(TrainingDataORM).filter_by(status='pending').limit(limit).all()
            return [TrainingSample.model_validate(r.__dict__) for r in records]
        finally:
            session.close()

    def mark_trained(self, ids):
        session = self.db.SessionLocal()
        try:
            session.query(TrainingDataORM).filter(TrainingDataORM.id.in_(ids)).update(
                {"status": "trained"}, synchronize_session=False
            )
            session.commit()
        finally:
            session.close()
