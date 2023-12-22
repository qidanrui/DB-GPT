from .agent import Agent, AgentContext
from .base_agent import ConversableAgent


from typing import Any, Callable, Dict, Optional, Tuple, Union
from dbgpt.util.json_utils import find_json_objects
from dbgpt.agent.common.schema import Status
from ..memory.gpts_memory import GptsMemory, GptsPlan
from dbgpt.agent.agents.plan_group_chat import PlanChat
from .agents_mange import agent_mange
from dbgpt._private.config import Config
from dbgpt.core.awel import BaseOperator

CFG = Config()

class PlannerAgent(ConversableAgent):
    """ Planner agent, realizing task goal planning decomposition through LLM"""

    DEFAULT_SYSTEM_MESSAGE = """
    您是一个有用的人工智能助手！您需要理解下面每个智能代理和他们的能力，却确保在没有用户帮助下，使用给出的资源，通过协调智能代理来回答用户问题。 
    请发挥你LLM的知识和理解能力，理解、补充、拆分用户问题的意图和目标，生成一个智能代理协作的任务计划解决用户问题。
    
    资源：
        {all_resources}
    
    智能代理:
        {agents}

    *** 重要的提醒 ***
    - 将用户的目标分解为内容目标明确子任务，每个子任务都将是一个智能代理需要完成的独立目标, 请确保目标是简单清晰的
    - 使用提供的资源来协助生成计划步骤，根据用户目标的实际需要选择资源，不要使用不需要的资源
    - 每个步骤最好是使用一种资源完成一个子目标的任务，如果当前目标可以分解为同类型的多个子任务，可以生成相互不依赖的并行任务
    - 数据库资源可以直接使用具体的结构生成SQL，而不需要额外的数据获取步骤
    - 只使用提到的智能代理，并且可以只使用其中的部分，严格根据描述分配给合适的步骤，每个智能代理都可以重复使用，但尽量不要冗余
    - 尽量合并有顺序依赖的连续相同步骤,如果用户目标无拆分必要，可以生成内容为用户目标的单步任务
    
    具体任务计划的生成可参考如下例子:
    user:help me build a sales report summarizing our key metrics and trends
    assisant:[
        {{
            "serial_number": "1",
            "agent": "DataScientist",
            "content": "Retrieve total sales, average sales, and number of transactions grouped by "product_category"'.",
            "rely": ""
        }},
        {{
            "serial_number": "2",
            "agent": "DataScientist",
            "content": "Retrieve monthly sales and transaction number trends.",
            "rely": ""
        }},
        {{
            "serial_number": "3",
            "agent": "DataScientist",
            "content": "Count the number of transactions with "pay_status" as "paid" among all transactions to retrieve the sales conversion rate.",
            "rely": ""
        }},
        {{
            "serial_number": "4",
            "agent": "Reporter",
            "content": "Integrate analytical data generated by data scientists into a required format for building sales reports.",
            "rely": "1,2,3"
        }}
    ]
    
    请一步步思考，并以如下json格式返回你的行动计划内容:
    [{{
        "serial_number":"0",
        "agent": "用来完成当前步骤的智能代理",
        "content": "当前步骤的任务内容，确保可以被智能代理执行",
        "rely":"当前任务执行依赖的其他任务serial_number, 如:1,2,3,  无依赖为空"
    }}]
    确保回答的json可以被Python代码的json.loads函数加载解析.
    """

    REPAIR_SYSTEM_MESSAGE = """
     您是规划专家!现在你需要利用你的专业知识，仔细检查已生成的计划,进行重新评估和分析，确保计划的每个步骤都是清晰完整的，可以被智能代理理解的，解决当前计划中遇到的问题！并按要求返回新的计划内容。
    """
    NAME = "Planner"
    def __init__(
            self,
            memory: GptsMemory,
            plan_chat: PlanChat,
            llm_operator: Optional[BaseOperator] = None,
            is_termination_msg: Optional[Callable[[Dict], bool]] = None,
            max_consecutive_auto_reply: Optional[int] = None,
            human_input_mode: Optional[str] = "NEVER",
            agent_context: 'AgentContext' = None,
            **kwargs,
    ):
        super().__init__(
            name=self.NAME,
            memory=memory,
            llm_operator=llm_operator,
            system_message=self.DEFAULT_SYSTEM_MESSAGE,
            is_termination_msg=is_termination_msg,
            max_consecutive_auto_reply=max_consecutive_auto_reply,
            human_input_mode=human_input_mode,
            agent_context=agent_context,
            **kwargs,
        )
        self.plan_chat = plan_chat
        ### register planning funtion
        self.register_reply(
            Agent,
            PlannerAgent._a_planning
        )


    agent_mange.all_agents()
    def build_param(self, agent_context: AgentContext):
        resources = []
        if agent_context.resource_db is not None:
            db_connect = CFG.LOCAL_DB_MANAGE.get_connect(agent_context.resource_db.get('name'))

            resources.append(f"{agent_context.resource_db.get('type')}:{agent_context.resource_db.get('name')}\n{db_connect.get_table_info()}")
        if agent_context.resource_knowledge is not None:
            resources.append(f"{agent_context.resource_knowledge.get('type')}:{agent_context.resource_knowledge.get('name')}\n{agent_context.resource_knowledge.get('introduce')}")
        if agent_context.resource_internet is not None:
            resources.append(f"{agent_context.resource_internet.get('type')}:{agent_context.resource_internet.get('name')}\n{agent_context.resource_internet.get('introduce')}")
        return {
            "all_resources": "\n".join([f"- {item}" for item in resources]),
            "agents": "\n".join([f"- {item}:{agent_mange.get_describe_by_name(item)}" for item in agent_context.agents]),
        }


    async def a_system_fill_param(self):
        params = self.build_param(self.agent_context)
        self.update_system_message(self.DEFAULT_SYSTEM_MESSAGE.format(**params))

    async def _a_planning(self,
                          message: Optional[str] = None,
                          sender: Optional[Agent] = None,
                          reviewer: "Agent" = None,
                          config: Optional[Any] = None,
                          ) -> Tuple[bool, Union[str, Dict, None]]:

        json_objects = find_json_objects(message)
        plan_objects = []
        fail_reason = "Please recheck your answer，no usable plans generated in correct format，"
        json_count = len(json_objects)
        rensponse_succ = True
        if json_count != 1:
            ### Answer failed, turn on automatic repair
            fail_reason += f"There are currently {json_count} json contents"
            rensponse_succ = False
        else:
            try:
                for item in json_objects[0]:
                    plan = GptsPlan(conv_id = self.agent_context.conv_id, sub_task_num = item.get('serial_number'), sub_task_content = item.get('content'))
                    plan.resource_name = item.get('resource')
                    plan.max_retry_times = self.agent_context.max_retry_round
                    plan.sub_task_agent = item.get('agent')
                    plan.sub_task_title = item.get('content')
                    plan.rely = item.get("rely")
                    plan.retry_times = 0
                    plan.status = Status.TODO.value
                    plan_objects.append(plan)
            except Exception as e:
                fail_reason += f"Return json structure error and cannot be converted to a usable plan，{str(e)}"
                rensponse_succ = False

        if rensponse_succ:
            if len(plan_objects) > 0:
                ### Delete the old plan every time before saving it
                self.memory.plans_memory.remove_by_conv_id(self.agent_context.conv_id)
                self.memory.plans_memory.batch_save(plan_objects)

            content = ".\n".join(
                ["{},{}".format(index + 1, item.get('content')) for index, item in enumerate(json_objects[0])])
        else:
            content = fail_reason
        return True, {"is_exe_success": rensponse_succ, "content": content, "view": content}