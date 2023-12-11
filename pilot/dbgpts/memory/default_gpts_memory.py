from typing import List, Optional
import pandas as pd
from dataclasses import fields
from .base import GptsPlansMemory, GptsPlan, GptsMessageMemory, GptsMessage
from pilot.common.schema import Status


class DefaultGptsPlansMemory(GptsPlansMemory):



    def __init__(self):
        self.df = pd.DataFrame(columns=[field.name for field in fields(GptsPlan)])

    def batch_save(self, plans: list[GptsPlan]):
        new_rows = pd.DataFrame([item.to_dict() for item in plans])
        self.df = pd.concat([self.df, new_rows], ignore_index=True)

    def get_by_conv_id(self, conv_id: str) -> List[GptsPlan]:
        result = self.df.query(f"conv_id=='{conv_id}'")
        plans = []
        for row in result.itertuples(index=False, name=None):
            row_dict = dict(zip(self.df.columns, row))
            plans.append(GptsPlan.from_dict(row_dict))
        return plans

    def get_by_conv_id_and_num(self, conv_id: str, task_nums: List[int]) -> List[GptsPlan]:
        result = self.df.query(f"conv_id=='{conv_id}' and sub_task_num in [{','.join(task_nums)}]")
        plans = []
        for row in result.itertuples(index=False, name=None):
            row_dict = dict(zip(self.df.columns, row))
            plans.append(GptsPlan.from_dict(row_dict))
        return plans

    def get_todo_plans(self, conv_id: str) -> List[GptsPlan]:
        result = self.df.query(f"conv_id=='{conv_id}' and state=='todo'")
        plans = []
        for row in result.itertuples(index=False, name=None):
            row_dict = dict(zip(self.df.columns, row))
            plans.append(GptsPlan.from_dict(row_dict))
        return plans

    def complete_task(self, conv_id: str, task_num: int, result: str):
        self.df.loc[(self.df['conv_id'] == conv_id) & (self.df['sub_task_num'] == task_num), ['state', 'result']] = {
            "state": Status.COMPLETED.value, "result": result}

    def update_task(self, conv_id: str, task_num: int, state: str, retry_times: int, agent: str = None, model=None):
        self.df.loc[(self.df['conv_id'] == conv_id) & (self.df['sub_task_num'] == task_num),
                    ['state', 'retry_times', 'sub_task_agent', 'agent_model']] = {"state": state,
                                                                                  "retry_times": retry_times,
                                                                                  "sub_task_agent": agent,
                                                                                  "agent_model": model}


    def remove_by_conv_id(self, conv_id: str):
        self.df.drop(self.df[self.df['conv_id']==conv_id].index, inplace=True)

class DefaultGptsMessageMemory(GptsMessageMemory):


    def __init__(self):
        self.df = pd.DataFrame(columns= [field.name for field in fields(GptsMessage)] )

    def append(self, message: GptsMessage):
        self.df.loc[len(self.df)] = message.to_dict()

    def get_by_agent(self, agent: str) -> Optional[List[GptsMessage]]:
        result = self.df.query(f"sender=='{agent}'and receiver=='{agent}'")
        messages = []
        for row in result.itertuples(index=False, name=None):
            row_dict = dict(zip(self.df.columns, row))
            messages.append(GptsMessage.from_dict(row_dict))
        return messages

    def get_between_agents(self, agent1: str, agent2: str) -> Optional[List[GptsMessage]]:
        result = self.df.query(f"(sender=='{agent1}' and receiver=='{agent2}') or (sender=='{agent2}' and receiver=='{agent1}')")
        messages = []
        for row in result.itertuples(index=False, name=None):
            row_dict = dict(zip(self.df.columns, row))
            messages.append(GptsMessage.from_dict(row_dict))
        return messages
