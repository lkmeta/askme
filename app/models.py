from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pgvector.sqlalchemy import Vector


Base = declarative_base()


# ORM model for FAQs stored in PostgreSQL
class FAQ(Base):
    __tablename__ = "faqs"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    embedding = Column(Vector(1536), nullable=True)
