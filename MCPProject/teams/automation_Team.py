from agents.TestCaseWriterAgent import getTestCasesWriterAgent
from agents.Playwright_Automation_Agent import getPlaywrightAutomationAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_ext.tools.mcp import McpWorkbench, StdioServerParams
import asyncio

playwright_mcp_server_params = StdioServerParams( 
    command="npx",
    args=[
        "@playwright/mcp@latest",
        "--isolated"
    ],
)

playwright_workbench = McpWorkbench(playwright_mcp_server_params)


async def get_MCP_team(model_client):
    test_cases_writer_agent = getTestCasesWriterAgent(model_client)

    playwright_automation_agent = await getPlaywrightAutomationAgent(
        model_client,
        playwright_workbench
    )

    text_mention_termination = TextMentionTermination("STOP")

    team = RoundRobinGroupChat(
        participants=[test_cases_writer_agent, playwright_automation_agent],
        max_turns=20,
        termination_condition=text_mention_termination,
    )
    return team