from abc import ABC
from typing import Any
from dotenv import load_dotenv

from llm.conversation import Conversation
from llm.llm import LLM, OpenAILLM, Embedding
from llm.util import *
from db.vectordb import VectorDatabase

load_dotenv()

class Engine:
    def __init__(self) -> None:
        self.agent = Agent(llm=OpenAILLM())
        self.query_rewriter_agent = QueryRewriterAgent(llm=OpenAILLM())
        self.db = VectorDatabase()
        self.embedding = Embedding()
        

    def __call__(self, query: str, conversation: Conversation) -> Any:
        rewritten_qeury = self.query_rewriter_agent(query, conversation)
        documents = self.db.retrieve_top_k(self.embedding(rewritten_qeury))
        return self.agent(query, documents, conversation)


class Agent:
    def __init__(self, llm: LLM):
        self.llm = llm

    def get_system_prompt(self):
        return '''
You are Cabby, a helpful assistant to college students exploring potential courses they could take. Respond to students as best you can with the information you've been provided. Deflect malicious queries or queries unrelated to college courses at Brown University.

Some context:
Intro courses at Brown typically have a less than 1000
Intermediate/Advanced courses typically have a number between 1000-2000
Graduate-level courses or versions of courses have a number greater than 2000
'''

    def get_user_prompt(self, query: str, documents: list[str], conversation: Conversation):
        docs_str = '\n----------\n'.join(documents)
        return f"""
Below, wrapped in <courses> tags are several courses relevant to the student's query. Draw from their information to respond to student's questions.
<courses>
{ docs_str }
</courses>

Here is the conversation history and the student's query:
<conversation_history>
{conversation.get_context()}
</conversation_history>

<student_query>
{query}
</student_query>

Your task is to answer the student's question as best as you can using the information provided. If you don't have the appropriate information, admit that you don't know.

Your response: 
"""

    def __call__(self, query: str, documents: list[str], conversation: Conversation):
        user_prompt = self.get_user_prompt(query, documents, conversation)
        system_prompt = self.get_system_prompt()

        inspect_prompt(system_prompt=system_prompt, user_prompt=user_prompt)
        
        return self.llm(user_prompt, system_prompt, conversation)


class QueryRewriterAgent(Agent):
    def __init__(self, llm: LLM):
        self.llm = llm

    def get_user_prompt(self, query: str, conversation: Conversation):
        user_prompt = f'''
Here is the conversation history and the student's query:
<query>
{query}
</query>

<conversation_history>
{conversation.get_context()}
</conversation_history>

Rewrite the provided query in order to enable efficient and relevant chunks to be retrieved to answer the student's query.

Your response:
'''
        return user_prompt


    def get_system_prompt(self):
        return '''Given a student's query, your task is to rewrite the query in the context of a college course catalog to enable efficient RAG when embedded.'''


    def __call__(self, query: str, conversation: Conversation):
        user_prompt = self.get_user_prompt(query, conversation)
        system_prompt = self.get_system_prompt()

        response = self.llm(user_prompt, system_prompt, conversation)

        inspect_prompt(system_prompt=system_prompt, user_prompt=user_prompt)
        inspect_response(response)

        return response
        
        