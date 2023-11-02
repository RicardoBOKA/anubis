from sqlalchemy import Table, Boolean, Column, ForeignKey, Integer, String, UniqueConstraint, ForeignKeyConstraint
from sqlalchemy.orm import relationship, column_property
from uuid import uuid4
from ..database import autocommit_engine, Base, SessionLocal


class Restriction(Base):
    __tablename__ = "restrictions"

    id = Column(String, primary_key=True, default=uuid4, index=True)
    name = Column(String, index=True)

    table_target_id = Column(String)

    def set_target(self, table_name, instance_id):
        self.table_target_id = f"{table_name}:{instance_id}"

    def get_target_name(self):
        return self.targetID[0]
    def get_target_id(self):
        return self.targetID[2:]


def init_db():
    Base.metadata.create_all(bind=autocommit_engine)


def drop_db():
    Base.metadata.drop_all(bind=autocommit_engine)
