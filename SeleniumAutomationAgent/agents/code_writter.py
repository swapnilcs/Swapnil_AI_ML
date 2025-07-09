from autogen_agentchat.agents import AssistantAgent
from models.openAIModel import model_client



code_writer = AssistantAgent(
        name = "Code_Writer_Agent",
        description = "An agent that generates python code",
        model_client=model_client,
        system_message='''
        Generate selenium UI test cases using python language.
        Selenium grid is up and running on localhost:4444/.
        Run these UI automation test cases on Chrome broser as this the browser set up on selenium grid.
        Make sure you have the Selenium library installed and ChromeDriver set up correctly on your system 
        to run this script. This code will connect to a Selenium Grid running locally and execute the test on a Chrome browser as specified.
        Also capture screenhots and logs for each step and store in current dir to view these screenshots and logs.
        Also make sure to quit the driver and browser at the end of the script.
        '''
    )





