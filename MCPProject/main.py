import asyncio
from config.open_ai_model_client import get_Model_Client
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult
from teams.automation_Team import get_MCP_team

async def main():
    openai_model_client = get_Model_Client()

    team = await get_MCP_team(openai_model_client)

    try:
        task = """
        Navigate to https://opensource-demo.orangehrmlive.com/web/index.php/auth/login
            and write 2 test cases.
            1. For login with valid credentials (username: Admin, password: admin123)
            2. For after login navigate to My Info page and update the first name and last name and save it.
        """

        async for message in team.run_stream(task=task):
            print('***' * 40)
            if isinstance(message, TextMessage):
                print(f"{message.source} says: {message.content}")
            elif isinstance(message, TaskResult):
                print("Stop reason:", message.stop_reason)

    except Exception as e:
        print("Error during team execution:", str(e))


if __name__ == "__main__":
    asyncio.run(main())



