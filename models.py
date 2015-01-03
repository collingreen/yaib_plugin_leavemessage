from sqlalchemy import Table, Column, String, DateTime, Text
from modules.persistence import Base, getModelBase


CustomBase = getModelBase('leavemessage')


class Message(Base, CustomBase):
    user = Column(String(200))
    nick = Column(String(100))
    message_time = Column(DateTime)
    to_nick = Column(String(100))
    channel = Column(String(50))
    message = Column(Text)
