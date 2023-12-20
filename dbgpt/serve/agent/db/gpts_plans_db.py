from datetime import datetime
from typing import List
from sqlalchemy import Column, Integer, String, Index, DateTime, func, Text
from sqlalchemy import UniqueConstraint

from dbgpt.storage.metadata import BaseDao
from dbgpt.storage.metadata.meta_data import (
    Base,
    engine,
    session,
    META_DATA_DATABASE,
)
from dbgpt.agent.common.schema import Status


class GptsPlansEntity(Base):
    __tablename__ = "gpts_plans"
    __table_args__ = {
        "mysql_charset": "utf8mb4",
        "mysql_collate": "utf8mb4_unicode_ci",
    }
    id = Column(Integer, primary_key=True, comment="autoincrement id")

    conv_id = Column(String(255), nullable=False, comment="The unique id of the conversation record")
    sub_task_num = Column(Integer, nullable=False, comment="Subtask number")
    sub_task_title = Column(String(255), nullable=False, comment="subtask title")
    sub_task_content = Column(Text, nullable=False, comment="subtask content")
    sub_task_agent = Column(String(255), nullable=True, comment="Available agents corresponding to subtasks")
    resource_name= Column(String(255), nullable=True, comment="resource name")
    rely = Column(String(255), nullable=True, comment="Subtask dependencies，like: 1,2,3")

    agent_model = Column(String(255), nullable=True, comment="LLM model used by subtask processing agents")
    retry_times = Column(Integer, default=False, comment="number of retries")
    max_retry_times = Column(Integer, default=False, comment="Maximum number of retries")
    state = Column(String(255), nullable=True, comment="subtask status")
    result = Column(Text(length=2 ** 31 - 1), nullable=True, comment="subtask result")

    created_at = Column(
        DateTime, default=datetime.utcnow, comment="create time"
    )
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="last update time"
    )
    __table_args__ = (
        UniqueConstraint("conv_id", "sub_task_num", name="uk_sub_task"),
    )



class GptsPlansDao(BaseDao[GptsPlansEntity]):
    def __init__(self):
        super().__init__(
            database=META_DATA_DATABASE,
            orm_base=Base,
            db_engine=engine,
            session=session,
        )

    def batch_save(self, plans: list[dict]):
        session = self.get_session()
        session.bulk_insert_mappings(GptsPlansEntity, plans)
        session.commit()
        session.close()

    def get_by_conv_id(self, conv_id: str) -> list[GptsPlansEntity]:
        session = self.get_session()
        gpts_plans = session.query(GptsPlansEntity)
        if conv_id:
            gpts_plans = gpts_plans.filter(GptsPlansEntity.conv_id == conv_id)
        result = gpts_plans.all()
        session.close()
        return result

    def get_by_task_id(self, task_id: int) -> list[GptsPlansEntity]:
        session = self.get_session()
        gpts_plans = session.query(GptsPlansEntity)
        if task_id:
            gpts_plans = gpts_plans.filter(GptsPlansEntity.id == task_id)
        result = gpts_plans.first()
        session.close()
        return result

    def get_by_conv_id_and_num(self, conv_id: str, task_nums: list) -> list[GptsPlansEntity]:
        session = self.get_session()
        gpts_plans = session.query(GptsPlansEntity)
        if conv_id:
            gpts_plans = gpts_plans.filter(GptsPlansEntity.conv_id == conv_id).filter(
                GptsPlansEntity.sub_task_num.in_(task_nums))
        result = gpts_plans.all()
        session.close()
        return result

    def get_todo_plans(self, conv_id: str) -> list[GptsPlansEntity]:
        session = self.get_session()
        gpts_plans = session.query(GptsPlansEntity)
        if not conv_id:
            return []
        gpts_plans = gpts_plans.filter(GptsPlansEntity.conv_id == conv_id).filter(
            GptsPlansEntity.state.in_(Status.TODO.value, Status.RETRYING.value))
        result = gpts_plans.order_by(GptsPlansEntity.sub_task_num).all()
        session.close()
        return result

    def complete_task(self, conv_id: str, task_num: int, result: str):
        session = self.get_session()
        gpts_plans = session.query(GptsPlansEntity)
        gpts_plans = gpts_plans.filter(GptsPlansEntity.conv_id == conv_id).filter(GptsPlansEntity.sub_task_num == task_num)
        gpts_plans.update({
            GptsPlansEntity.state: Status.COMPLETE.value,
            GptsPlansEntity.result: result
        }, synchronize_session='fetch')
        session.commit()
        session.close()

    def update_task(self, conv_id: str, task_num: int, state: str, retry_times: int, agent: str = None, model: str = None, result:str = None):
        session = self.get_session()
        gpts_plans = session.query(GptsPlansEntity)
        gpts_plans = gpts_plans.filter(
            GptsPlansEntity.conv_id == conv_id).filter(
            GptsPlansEntity.sub_task_num == task_num)
        gpts_plans.update({
            GptsPlansEntity.state: state,
            GptsPlansEntity.sub_task_agent: agent,
            GptsPlansEntity.agent_model: model,
            GptsPlansEntity.retry_times: retry_times,
            GptsPlansEntity.result: result
        }, synchronize_session='fetch')
        session.commit()
        session.close()

    def remove_by_conv_id(self, conv_id: str):
        session = self.get_session()
        if conv_id is None:
            raise Exception("conv_id is None")

        gpts_plans = session.query(GptsPlansEntity)
        gpts_plans.filter(GptsPlansEntity.conv_id == conv_id).delete()
        session.commit()
        session.close()
