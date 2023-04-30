from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    and_,
    create_engine,
)
from sqlalchemy.exc import MultipleResultsFound
from sqlalchemy.orm import DeclarativeBase, scoped_session, sessionmaker  # type: ignore

DB_URL = "sqlite:///reviewbot.db"
engine = create_engine(DB_URL, echo=True)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


class Base(DeclarativeBase):
    ...


class Reviews(Base):
    __tablename__ = "reviews"

    key_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    message = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.__class__}, {self.user_id}"


class Photos(Base):
    __tablename__ = "photos"

    key_id = Column(Integer, primary_key=True)
    photo_data = Column(String)
    review_id = Column(Integer, ForeignKey("reviews.key_id"))


@dataclass
class DBCtrl:
    @classmethod
    def create_review_record(cls, user_id: int):
        with Session() as session:
            session.add(Reviews(user_id=user_id))
            session.commit()

    @classmethod
    def update_review_message(cls, user_id: int, message):
        with Session() as session:
            record = (
                session.query(Reviews)
                .where(and_(Reviews.user_id == user_id, Reviews.message == None))
                .one_or_none()
            )
            if record is not None:
                record.message = message
                session.commit()

    @classmethod
    def get_review_without_message(cls, user_id: int):
        with Session() as session:
            return (
                session.query(Reviews)
                .where(and_(Reviews.message == None, Reviews.user_id == user_id))
                .one_or_none()
            )

    @classmethod
    def get_all_reviews(cls) -> list[Reviews]:
        with Session() as session:
            return session.query(Reviews).all()

    @classmethod
    def get_photos(cls):
        with Session() as session:
            return session.query(Photos).all()

    @classmethod
    def get_photo_by_review_id(cls, review_id):
        with Session() as session:
            try:
                return (
                    session.query(Photos)
                    .where(Photos.review_id == review_id)
                    .one_or_none()
                )
            except MultipleResultsFound:
                return (
                    session.query(Photos).where(Photos.review_id == review_id).first()
                )

    @classmethod
    def create_photo(cls, photo_data, review_id):
        with Session() as session:
            session.add(Photos(photo_data=str(photo_data), review_id=review_id))
            session.commit()

    @classmethod
    def create_tables(cls):
        Base.metadata.create_all(bind=engine)


# if __name__ == "__main__":
#     DBCtrl.create_tables()
