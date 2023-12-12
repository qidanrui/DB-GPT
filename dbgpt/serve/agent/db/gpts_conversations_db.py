from datetime import datetime
from typing import List
from sqlalchemy import Column, Integer, String, Index, DateTime, func, Text, desc
from sqlalchemy import UniqueConstraint

from dbgpt.storage.metadata import BaseDao
from dbgpt.storage.metadata.meta_data import (
    Base,
    engine,
    session,
    META_DATA_DATABASE,
)


class GptsConversationsEntity(Base):
    __tablename__ = "gpts_conversations"
    __table_args__ = {
        "mysql_charset": "utf8mb4",
        "mysql_collate": "utf8mb4_unicode_ci",
    }
    id = Column(Integer, primary_key=True, comment="autoincrement id")

    conv_id = Column(String(255), nullable=True, comment="The unique id of the conversation record")
    user_goal = Column(Text, nullable=True, comment="User's goals content")

    gpts_name = Column(String(255), nullable=True, comment="The gpts name")
    state = Column(String(255), nullable=True, comment="The gpts state")

    max_auto_reply_round = Column(Integer, nullable=False, comment="max auto reply round")
    auto_reply_count = Column(Integer, nullable=False, comment="auto reply count")

    user_code = Column(String(255), nullable=False, comment="user code")
    system_app = Column(String(255), nullable=True, comment="system app ")

    created_at = Column(
        DateTime, default=datetime.utcnow, comment="create time"
    )
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="last update time"
    )

    UniqueConstraint("conv_id", name="uk_gpts_conversations")
    Index("idx_q_gpts", "gpts_name")
    Index("idx_q_content", "goal_introdiction")


class GptsConversationsDao(BaseDao[GptsConversationsEntity]):
    def __init__(self):
        super().__init__(
            database=META_DATA_DATABASE,
            orm_base=Base,
            db_engine=engine,
            session=session,
        )

    def add(self, engity: GptsConversationsEntity):
        session = self.get_session()
        session.add(engity)
        session.commit()
        id = engity.id
        session.close()
        return id

    def get_convs(self, user_code: str = None, system_app: str = None):
        session = self.get_session()
        gpts_conversations = session.query(GptsConversationsEntity)
        if user_code:
            gpts_conversations = gpts_conversations.filter(GptsConversationsEntity.user_code == user_code)
        if system_app:
            gpts_conversations = gpts_conversations.filter(GptsConversationsEntity.system_app == system_app)

        result = gpts_conversations.limit(20).order_by(desc(GptsConversationsEntity.id)).all()
        session.close()
        return result
