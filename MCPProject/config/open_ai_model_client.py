from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

def get_Model_Client():    
    """
    Function to get OpenAI model client.
    This client will be used to interact with OpenAI models.
    """ 
    openai_model_client = OpenAIChatCompletionClient(
        model="gpt-4o",
        api_key=api_key       
    )
    return openai_model_client