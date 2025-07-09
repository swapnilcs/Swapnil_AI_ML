from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import TextMessage
from dotenv import load_dotenv
import os
from autogen_core import CancellationToken
from autogen_agentchat.ui import Console
from pydantic import BaseModel, Field
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
import asyncio
from autogen_agentchat.agents import CodeExecutorAgent
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from autogen_agentchat.base import TaskResult
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
from autogen_core.code_executor import CodeBlock
from autogen_ext.tools.code_execution import PythonCodeExecutionTool


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = 'gpt-4o'
MAX_TURNS = 5
TERMINATION_WORD = "STOP"
