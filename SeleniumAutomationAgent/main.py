from autogen_agentchat.messages import TextMessage
from teams.teams import team
from autogen_agentchat.base import TaskResult
import asyncio



async def main():
    task = task = input('Enter your task here :- ' ) #"Navigate to Amazon.in and search for iphone 16 pro max"
    async for message in team.run_stream(task=task):
            if isinstance(message, TextMessage):
                print("***" * 30)
                print(message.source, ":" , message)
                print("%%%" * 30)
            elif isinstance(message, TaskResult):
                print('Stop Reason :', message.stop_reason)
                
if __name__ == "__main__":
    asyncio.run(main())
    

    