from __future__ import annotations

from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass, asdict, fields
import dataclasses
from ..memory.gpts_memory import GptsMemory


class Agent:
    """
    An interface for AI agent.
    An agent can communicate with other agents and perform actions.
    """

    def __init__(
        self,
        name: str,
        memory: GptsMemory,
        describe: str,
    ):
        """
        Args:
            name (str): name of the agent.
        """
        self._name = name
        self._describe = describe

        # the agent's collective memory
        self._memory = memory

    @property
    def name(self):
        """Get the name of the agent."""
        return self._name

    @property
    def memory(self):
        return self._memory

    @property
    def describe(self):
        """Get the name of the agent."""
        return self._describe

    async def a_send(
        self,
        message: Union[Dict, str],
        recipient: "Agent",
        reviewer: "Agent",
        request_reply: Optional[bool] = None,
    ):
        """(Abstract async method) Send a message to another agent."""


    async def a_receive(
        self,
        message: Union[Dict],
        sender: "Agent",
        reviewer: "Agent",
        request_reply: Optional[bool] = None,
        silent: Optional[bool] = False
    ):
        """(Abstract async method) Receive a message from another agent."""



    async def a_review(self,   message: Union[Dict, str], censored:"Agent"):
        """

        Args:
            message:
            censored:

        Returns:

        """

    def reset(self):
        """(Abstract method) Reset the agent."""


    async def a_generate_reply(
        self,
        messages: Optional[List[Dict]] = None,
        sender: Optional["Agent"] = None,
        **kwargs,
    ) -> Union[str, Dict, None]:
        """(Abstract async method) Generate a reply based on the received messages.

        Args:
            messages (list[dict]): a list of messages received.
            sender: sender of an Agent instance.
        Returns:
            str or dict or None: the generated reply. If None, no reply is generated.
        """

    async def a_reasoning_reply(
        self,
        messages: Union[List[str]],
        sender: "Agent",
        reviewer: "Agent",
        request_reply: Optional[bool] = None,
        silent: Optional[bool] = False)-> Union[str, Dict, None]:
        """
        Based on the requirements of the current agent, reason about the current task goal through LLM
        Args:
            message:
            sender:
            reviewer:
            request_reply:
            silent:

        Returns:
            str or dict or None: the generated reply. If None, no reply is generated.
        """


    async def a_action_reply(
        self,
        messages: Optional[str],
        sender: "Agent",
        **kwargs,
    ) -> Union[str, Dict, None]:
        """
        Parse the inference results for the current target and execute the inference results using the current agent's executor
        Args:
            messages (list[dict]): a list of messages received.
            sender: sender of an Agent instance.
            **kwargs:
        Returns:
             str or dict or None: the agent action reply. If None, no reply is generated.
        """

    async def a_verify_reply(
        self,
        action_reply: Optional[Dict],
        sender: "Agent",
        **kwargs,
    ) -> Union[str, Dict, None]:
        """
        Verify whether the current execution results meet the target expectations
        Args:
            messages:
            sender:
            **kwargs:

        Returns:

        """


@dataclass
class AgentResource:
    type: str
    name: str
    introduce: str

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> AgentResource:
        if d is None: return None
        return AgentResource(
            type=d.get("type"),
            name=d.get("name"),
            introduce=d.get("introduce"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return dataclasses.asdict(self)

@dataclass
class AgentContext:
    conv_id: str
    gpts_name: Optional[str]

    resource_db: Optional[AgentResource] = None
    resource_knowledge: Optional[AgentResource] = None
    resource_internet: Optional[AgentResource] = None
    llm_models: Optional[List[str]] = None
    agents: Optional[List[str]] = None

    max_chat_round: Optional[int] = 50
    max_retry_round: Optional[int] = 3
    max_new_tokens:Optional[int] = 1024
    temperature:Optional[float] = 0.5
    allow_format_str_template:Optional[bool] = False


    def to_dict(self) -> Dict[str, Any]:
        return dataclasses.asdict(self)