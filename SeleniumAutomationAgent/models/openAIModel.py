from config.settings import OPENAI_API_KEY,MODEL,TERMINATION_WORD,MAX_TURNS
from autogen_ext.models.openai import OpenAIChatCompletionClient



model_client = OpenAIChatCompletionClient(
    model= MODEL,
    open_api_key = OPENAI_API_KEY
)