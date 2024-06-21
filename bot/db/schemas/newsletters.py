from bot.db.db import Base
from sqlalchemy import Column, String, Integer, Boolean


class Newsletters(Base):
    __tablename__ = "newsletters"
    id = Column(Integer, autoincrement=True, primary_key=True)
    group_name = Column(String)
    group_id = Column(Integer)
    mailing_times = Column(String)
    text = Column(String)
    status = Column(Boolean)
