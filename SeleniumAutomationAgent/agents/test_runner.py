from autogen_agentchat.agents import AssistantAgent
from models.openAIModel import model_client
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
from autogen_ext.tools.code_execution import PythonCodeExecutionTool



executor = LocalCommandLineCodeExecutor(
        timeout=60,
        work_dir="code_exec_workspace",
        virtual_env_context=None  # optional: pass a venv context if desired
    )
    

tool = PythonCodeExecutionTool(executor)


test_runner = AssistantAgent(
        name = "Test_Runner_Agent",
        description = "An agent that runs python code on local",
        model_client=model_client,
        tools=[tool],
        reflect_on_tool_use=True,
        system_message='''
        You are an expert in running and executing python code.
        A Selenium Grid is running at http://localhost:4444/wd/hub
        Your job is to run these test cases.
        Save screenshots and logs in the current dir.
        In the end once the code is executed successfully, you have to say "STOP".
        '''
)