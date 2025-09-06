from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent
from agents.prompts.AgentPrompts import AUTOMATION_AGENT_PROMPT
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
import asyncio
from autogen_ext.tools.mcp import McpWorkbench
from autogen_ext.tools.mcp import StdioServerParams





async def getPlaywrightAutomationAgent(model_client, playwright_workbench):
    async with playwright_workbench as pw_wb:
        playwright_automation_agent = AssistantAgent(
            name="AutomationAgent",
            model_client=model_client,
            workbench=pw_wb,
            system_message=AUTOMATION_AGENT_PROMPT
        )
        return playwright_automation_agent



