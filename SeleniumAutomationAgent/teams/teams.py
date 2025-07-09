from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from agents.code_writter import code_writer
from agents.test_runner import test_runner
from config.settings import TERMINATION_WORD
from config.settings import MAX_TURNS


termination_condition = TextMentionTermination(TERMINATION_WORD)
    
team = RoundRobinGroupChat(
        participants=[code_writer,test_runner],
        termination_condition=termination_condition,
        max_turns=MAX_TURNS
)