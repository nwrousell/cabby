from abc import ABC
from dotenv import load_dotenv

from openai import OpenAI

load_dotenv()

openai_client = OpenAI()

class Conversation:
    def __init__(self, messages: list[dict] = None):
        self.messages = messages if messages is not None else []
    
    def add_message(self, message: str, role: str):
        self.messages.append({ 'message': message, 'role': role })

class OpenAILLM:
    def __init__(self, model='gpt-4o-mini', stream=False):
        self.model = model
        self.stream=stream
    
    def get_message_history(self, conversation: Conversation):
        message_history = []
        
        for message in conversation.messages:
            message_history.append({ 'role': message['role'], 'content': [{ 'type': 'text', 'text': message['message'] }] })
        
        return message_history
    
    def __call__(self, user_prompt: str, system_prompt: str, conversation: Conversation):
        messages = self.get_message_history(conversation)
        messages.insert(0, { 'role': 'system', 'content': [{ 'type': 'text', 'text': system_prompt }] })
        messages.append({'role': 'user', 'content': [{'type': 'text', 'text': user_prompt}]})
        response = openai_client.chat.completions.create(
                model=self.model,
                # max_tokens=llm_args.max_tokens,
                # temperature=llm_args.temperature,
                messages=messages,
                stream=self.stream,
            )
        return response.choices[0].message.content


# class to abstract inserting context into prompt
class Agent:
    def __init__(self, llm: OpenAILLM):
        self.llm = llm

    def get_system_prompt(self):
        return 'You are Cabby, a helpful assistant to college students exploring potential courses they could take.'

    def get_user_prompt(self, documents: list[str]):
        docs_str = '\n----------\n'.join(documents)
        return f"""
    Below, wrapped in <courses> tags are several courses relevant to the student's query. Use them to answer the student's question.
    
    <courses>
    { docs_str }
    </courses>
    
    Be honest about the popularity, time requirement, and professor effectiveness of the courses.
    
    Response: 
"""

    def __call__(self, documents: list[str], conversation: Conversation):
        user_prompt = self.get_user_prompt(documents)
        system_prompt = self.get_system_prompt()
        
        return self.llm(user_prompt, system_prompt, conversation)