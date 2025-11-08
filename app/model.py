from sqlalchemy import (create_engine, Column, Integer, String,
                        and_, NUMERIC, or_, CheckConstraint, Text)
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("postgresql://postgres:1@localhost:5432/postgres",
                       echo=True)
Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
db = Session()
Base = declarative_base()


class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, autoincrement=True)
    image = Column(String)
    title = Column(String, nullable=False)
    about = Column(String)
    price = Column(NUMERIC(9, 2))
    review = Column(Integer,
                    CheckConstraint('review BETWEEN 1 AND 5'),
                    default=1)


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    gmail = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    confirm_password = Column(String, nullable=False)



class Contact(Base):
    __tablename__ = "contact"
    id = Column(Integer, primary_key=True, autoincrement=True)
    gmail = Column(String, nullable=False, unique=True)
    phone_number = Column(String, nullable=False)
    text = Column(Text)



Base.metadata.create_all(engine)
