from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnableLambda

_histories={}
def history(session_id):
    return _histories.setdefault(session_id, InMemoryChatMessageHistory())

def add_turn(session_id,user,assistant):
    h=history(session_id)
    h.add_user_message(user)
    h.add_ai_message(assistant)

def get_messages(session_id):
    return history(session_id).messages
