from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent
from agents.prompts.AgentPrompts import TEST_CASES_WRITER_AGENT_PROMPT

def getTestCasesWriterAgent(model_client):
    """
    Function to get Data Analyzer Agent.
    This agent is responsible for analyzing the data and generating insights.
    It will work with code executor agent to execute the code.
    """    
    test_cases_writer_agent = AssistantAgent(
        name="TestCasesWriter",
        model_client=model_client,
        system_message=TEST_CASES_WRITER_AGENT_PROMPT
    )
    return test_cases_writer_agent