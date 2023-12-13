from typing import Any

from exchangelib import Credentials, Account, EWSDateTime
from sqlalchemy import create_engine, Column, Integer, String, Float, ARRAY, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from functools import wraps
import hashlib
import time

from api import sent_messages_count, received_messages_count, recipient_counts, bcc_count, cc_count, \
    read_messages_later_than, days_between_received_and_read, replied_messages_count, sent_characters_count, \
    messages_outside_working_hours, received_to_sent_ratio, bytes_received_to_sent_ratio, \
    messages_with_question_and_no_reply, tz

DATABASE_URI = 'postgresql://ldt_user:vyQGA2R2GCVLOZyfv104@178.170.196.177:5433/ldt_db'
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class UserStatistics(Base):
    __tablename__ = "user_statistics"

    user_hash = Column(String, primary_key=True)
    sent_messages_count = Column(Integer)
    received_messages_count = Column(Integer)
    recipient_counts = Column(Integer)
    bcc_count = Column(Integer)
    cc_count = Column(Integer)
    days_between_received_and_read = Column(ARRAY(Integer))
    replied_messages_count = Column(Integer)
    sent_characters_count = Column(Integer)
    messages_outside_working_hours = Column(Integer)
    received_to_sent_ratio = Column(Float)
    bytes_received_to_sent_ratio = Column(Float)
    messages_with_question_and_no_reply = Column(Integer)

    def __init__(self, login, password, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.user_hash = hashlib.sha256(f"{login}/{password}".encode("utf-8")).hexdigest()

    def __repr__(self):
        return '\n'.join(
        ["-" * 50,
        f"User Hash: {self.user_hash}",
        f"Sent Messages Count: {self.sent_messages_count}",
        f"Received Messages Count: {self.received_messages_count}",
        f"Recipient Counts: {self.recipient_counts}",
        f"BCC Count: {self.bcc_count}",
        f"CC Count: {self.cc_count}",
        f"Days Between Received and Read: {self.days_between_received_and_read}",
        f"Replied Messages Count: {self.replied_messages_count}",
        f"Sent Characters Count: {self.sent_characters_count}",
        f"Messages Outside Working Hours: {self.messages_outside_working_hours}",
        f"Received to Sent Ratio: {self.received_to_sent_ratio}",
        f"Bytes Received to Sent Ratio: {self.bytes_received_to_sent_ratio}",
        f"Messages With Question and No Reply: {self.messages_with_question_and_no_reply}",
        ])


def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        time_elapsed = end_time - start_time
        print(f"Функция {func.__name__} исполнилась за {time_elapsed:.6f} секунд(ы).")
        return result
    return wrapper


@timing_decorator
def create_table():
    Base.metadata.create_all(engine)


@timing_decorator
def create_user_statistics(login,
                           password,
                           start_date=EWSDateTime(2021, 1, 1, tzinfo=tz),
                           end_date=EWSDateTime(2025, 12, 31, tzinfo=tz)) -> str:
    user_hash = None
    with Session() as session:
        user_statistics = UserStatistics(login, password)
        user_hash = user_statistics.user_hash
        credentials = Credentials(login, password)
        account = Account(primary_smtp_address=login, credentials=credentials, autodiscover=True, access_type='delegate')

        sent_messages = list(filter(lambda v: v is not None, account.sent.filter(datetime_received__range=(start_date, end_date))))
        received_messages = list(filter(lambda v: v is not None, account.inbox.filter(datetime_received__range=(start_date, end_date))))

        for key, value in [
            ("sent_messages_count", sent_messages_count(account)),
            ("received_messages_count", received_messages_count(account)),
            ("recipient_counts", recipient_counts(sent_messages)),
            ("bcc_count", bcc_count(sent_messages)),
            ("cc_count", cc_count(sent_messages)),
            ("read_messages_later_than", read_messages_later_than(received_messages, 4)),
            ("days_between_received_and_read", days_between_received_and_read(received_messages)),
            ("replied_messages_count", replied_messages_count(account, received_messages)),
            ("sent_characters_count", sent_characters_count(sent_messages)),
            ("messages_outside_working_hours", messages_outside_working_hours(sent_messages)),
            ("received_to_sent_ratio", received_to_sent_ratio(len(received_messages), len(sent_messages))),
            ("bytes_received_to_sent_ratio", bytes_received_to_sent_ratio(received_messages, sent_messages)),
            ("messages_with_question_and_no_reply", messages_with_question_and_no_reply(account, received_messages)),
        ]:
            setattr(user_statistics, key, value)
        session.add(user_statistics)
        session.commit()
    return user_hash


@timing_decorator
def read_user_statistics(user_hash):
    with Session() as session:
        user_statistics = session.query(UserStatistics).filter_by(user_hash=user_hash).first()
    return user_statistics


@timing_decorator
def update_user_statistics(user_hash, **kwargs):
    with Session() as session:
        user_statistics = session.query(UserStatistics).filter_by(user_hash=user_hash).first()
        if user_statistics:
            for key, value in kwargs.items():
                setattr(user_statistics, key, value)
            session.commit()


@timing_decorator
def delete_user_statistics(user_hash):
    with Session() as session:
        session.query(UserStatistics).filter_by(user_hash=user_hash).delete()
        session.commit()


@timing_decorator
def read_all_user_statistics():
    with Session() as session:
        all_user_statistics = session.execute(select(UserStatistics)).scalars().all()
    return all_user_statistics


if __name__ == "__main__":
    delete_user_statistics('6c84dc10af7c2d562e45e7c86611910667676fad819ab899c438d34214b164a7')
    delete_user_statistics('8225ed958b28baf5c2c2df7eabb3780bf4abea270285fd404103b1aa0ceba18e')

    user_hash = create_user_statistics(
        "galimovdv@outlook.com", "MRC-qCm-6ec-FKN",
    )

    # user_data = read_user_statistics(user_hash)
    # print(f"user_data = \n{user_data}")

    # update_user_statistics(user_hash, sent_messages_count=20)

    all_users = read_all_user_statistics()
    for user in all_users:
        print(user)
