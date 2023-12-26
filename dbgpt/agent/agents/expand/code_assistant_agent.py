import json
from typing import Any, Callable, Dict, List, Literal, Optional, Tuple, Type, Union

from dbgpt.core.awel import BaseOperator
from dbgpt.util.code_utils import UNKNOWN, execute_code, extract_code, infer_lang
from dbgpt.util.string_utils import str_to_bool

from ...memory.gpts_memory import GptsMemory
from ..agent import Agent
from ..base_agent import ConversableAgent
from dbgpt.core.interface.message import ModelMessageRoleType

try:
    from termcolor import colored
except ImportError:

    def colored(x, *args, **kwargs):
        return x


class CodeAssistantAgent(ConversableAgent):
    """(In preview) Assistant agent, designed to solve a task with LLM.

    AssistantAgent is a subclass of ConversableAgent configured with a default system message.
    The default system message is designed to solve a task with LLM,
    including suggesting python code blocks and debugging.
    `human_input_mode` is default to "NEVER"
    and `code_execution_config` is default to False.
    This agent doesn't execute code by default, and expects the user to execute the code.
    """

    DEFAULT_SYSTEM_MESSAGE = """You are a helpful AI assistant.
Solve tasks using your coding and language skills.
In the following cases, suggest python code (in a python coding block) or shell script (in a sh coding block) for the user to execute.
    1. When you need to collect info, use the code to output the info you need, for example, browse or search the web, download/read a file, print the content of a webpage or a file, get the current date/time, check the operating system. After sufficient info is printed and the task is ready to be solved based on your language skill, you can solve the task by yourself.
    2. When you need to perform some task with code, use the code to perform the task and output the result. Finish the task smartly.
Solve the task step by step if you need to. Be clear which step uses code, and which step uses your language skill.
When using code, you must indicate the script type in the code block. The user cannot provide any other feedback or perform any other action beyond executing the code you suggest. The user can't modify your code. So do not suggest incomplete code which requires users to modify. Don't use a code block if it's not intended to be executed by the user.
If you want the user to save the code in a file before executing it, put # filename: <filename> inside the code block as the first line. Don't include multiple code blocks in one response. Do not ask users to copy and paste the result. Instead, use 'print' function for the output when relevant. Check the execution result returned by the user.
If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try.
Unless necessary, use python code first to solve the problem. If data is stored in a file, the file path and related content need to be output concisely use the "Print".
When you find an answer, verify the answer carefully. Please try to simplify the output of the code to ensure that the output data of the code you generate is concise and complete.
    """
    CHECK_RESULT_SYSTEM_MESSAGE = f"""
    You are an expert in analyzing artificial intelligence task results.
    Your responsibility is to analyze the task goals and execution results provided by the user, and then make judgments. You need to answer according to the following rules:
        Rule 1: Analysis and judgment only focus on whether the execution results are related to the task objectives, not whether the content of the results is reasonable.
        Rule 2: If the target is a calculation type, there is no need to verify the correctness of the numerical calculations in the execution results. As long as reasonable numbers are given, the answer is considered.
    As long as the execution result meets the task goal according to the above rules, True will be returned, otherwise False will be returned. Only returns True or False.
    """

    NAME = "CodeEngineer"
    DEFAULT_DESCRIBE = """According to the current planning steps, write python/shell code to solve the problem, such as: data crawling, data sorting and conversion, etc. Wrap the code in a code block of the specified script type. Users cannot modify your code. So don't suggest incomplete code that needs to be modified by others.
          Don't include multiple code blocks in one response. Don't ask others to copy and paste the results
    """

    def __init__(
        self,
        agent_context: "AgentContext",
        memory: GptsMemory = None,
        describe: Optional[str] = DEFAULT_DESCRIBE,
        is_termination_msg: Optional[Callable[[Dict], bool]] = None,
        max_consecutive_auto_reply: Optional[int] = None,
        human_input_mode: Optional[str] = "NEVER",
        code_execution_config: Optional[Union[Dict, Literal[False]]] = None,
        **kwargs,
    ):
        """
        Args:
            name (str): agent name.
            system_message (str): system message for the ChatCompletion inference.
                Please override this attribute if you want to reprogram the agent.
            llm_config (dict): llm inference configuration.
                Please refer to [OpenAIWrapper.create](/docs/reference/oai/client#create)
                for available options.
            is_termination_msg (function): a function that takes a message in the form of a dictionary
                and returns a boolean value indicating if this received message is a termination message.
                The dict can contain the following keys: "content", "role", "name", "function_call".
            max_consecutive_auto_reply (int): the maximum number of consecutive auto replies.
                default to None (no limit provided, class attribute MAX_CONSECUTIVE_AUTO_REPLY will be used as the limit in this case).
                The limit only plays a role when human_input_mode is not "ALWAYS".
            **kwargs (dict): Please refer to other kwargs in
                [ConversableAgent](conversable_agent#__init__).
        """
        super().__init__(
            name=self.NAME,
            memory=memory,
            describe=describe,
            system_message=self.DEFAULT_SYSTEM_MESSAGE,
            is_termination_msg=is_termination_msg,
            max_consecutive_auto_reply=max_consecutive_auto_reply,
            human_input_mode=human_input_mode,
            agent_context=agent_context,
            **kwargs,
        )
        self._code_execution_config: Union[Dict, Literal[False]] = (
            {} if code_execution_config is None else code_execution_config
        )
        ### register code funtion
        self.register_reply(Agent, CodeAssistantAgent.generate_code_execution_reply)

    def _vis_code_idea(self, code, exit_success, log, language):
        param = {}
        param["exit_success"] = exit_success
        param["language"] = language
        param["code"] = code
        param["log"] = log

        return f"```vis-code\n{json.dumps(param)}\n```"

    async def generate_code_execution_reply(
        self,
        message: Optional[str] = None,
        sender: Optional[Agent] = None,
        reviewer: "Agent" = None,
        config: Optional[Union[Dict, Literal[False]]] = None,
    ):
        """Generate a reply using code execution."""
        code_execution_config = (
            config if config is not None else self._code_execution_config
        )
        if code_execution_config is False:
            return False, None

        last_n_messages = code_execution_config.pop("last_n_messages", 1)

        # iterate through the last n messages reversly
        # if code blocks are found, execute the code blocks and return the output
        # if no code blocks are found, continue

        code_blocks = extract_code(message)

        if len(code_blocks) < 1:
            self.send(
                f"Failed to get valid answer,{message}", sender, None, silent=True
            )
        elif len(code_blocks) > 1 and code_blocks[0][0] == UNKNOWN:
            self.send(
                f"Failed to get valid answer,{message}", self, reviewer, silent=True
            )

        # found code blocks, execute code and push "last_n_messages" back
        exitcode, logs = self.execute_code_blocks(code_blocks)
        code_execution_config["last_n_messages"] = last_n_messages
        exit_success = True if exitcode == 0 else False
        if exit_success:
            return True, {
                "is_exe_success": exit_success,
                "content": f"{logs}",
                "view": self._vis_code_idea(
                    code_blocks, exit_success, logs, code_blocks[0][0]
                ),
            }
        else:
            return True, {
                "is_exe_success": exit_success,
                "content": f"exitcode: {exitcode} (execution failed)\n {logs}",
                "view": self._vis_code_idea(
                    code_blocks, exit_success, logs, code_blocks[0][0]
                ),
            }

    async def a_verify(self, message: Optional[Dict]):
        self.update_system_message(self.CHECK_RESULT_SYSTEM_MESSAGE)
        task_gogal = message.get("current_gogal", None)
        action_report = message.get("action_report", None)
        task_result = ""
        if action_report:
            task_result = action_report.get("content", "")

        check_reult, model = await self.a_reasoning_reply(
            [
                {
                    "role":  ModelMessageRoleType.HUMAN,
                    "content": f"""Please understand the following task objectives and results and give your judgment:
                        Task Gogal: {task_gogal}
                        Execution Result: {task_result}
                    Only True or False is returned.
                    """,
                }
            ]
        )
        sucess = str_to_bool(check_reult)
        fail_reason = None
        if sucess == False:
            fail_reason = "The execution result of the code you wrote is judged as not answering the task question. Please re-understand and complete the task."
        return sucess, fail_reason

    @property
    def use_docker(self) -> Union[bool, str, None]:
        """Bool value of whether to use docker to execute the code,
        or str value of the docker image name to use, or None when code execution is disabled.
        """
        return (
            None
            if self._code_execution_config is False
            else self._code_execution_config.get("use_docker")
        )

    def run_code(self, code, **kwargs):
        """Run the code and return the result.

        Override this function to modify the way to run the code.
        Args:
            code (str): the code to be executed.
            **kwargs: other keyword arguments.

        Returns:
            A tuple of (exitcode, logs, image).
            exitcode (int): the exit code of the code execution.
            logs (str): the logs of the code execution.
            image (str or None): the docker image used for the code execution.
        """
        return execute_code(code, **kwargs)

    def execute_code_blocks(self, code_blocks):
        """Execute the code blocks and return the result."""
        logs_all = ""
        for i, code_block in enumerate(code_blocks):
            lang, code = code_block
            if not lang:
                lang = infer_lang(code)
            print(
                colored(
                    f"\n>>>>>>>> EXECUTING CODE BLOCK {i} (inferred language is {lang})...",
                    "red",
                ),
                flush=True,
            )
            if lang in ["bash", "shell", "sh"]:
                exitcode, logs, image = self.run_code(
                    code, lang=lang, **self._code_execution_config
                )
            elif lang in ["python", "Python"]:
                if code.startswith("# filename: "):
                    filename = code[11 : code.find("\n")].strip()
                else:
                    filename = None
                exitcode, logs, image = self.run_code(
                    code,
                    lang="python",
                    filename=filename,
                    **self._code_execution_config,
                )
            else:
                # In case the language is not supported, we return an error message.
                exitcode, logs, image = (
                    1,
                    f"unknown language {lang}",
                    None,
                )
                # raise NotImplementedError
            if image is not None:
                self._code_execution_config["use_docker"] = image
            logs_all += "\n" + logs
            if exitcode != 0:
                return exitcode, logs_all
        return exitcode, logs_all
