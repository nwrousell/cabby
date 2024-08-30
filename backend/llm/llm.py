
import os
from abc import ABC, abstractmethod
from typing import Any
from dotenv import load_dotenv
from time import time

import openai

from llm.util import *

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)

print(OPENAI_API_KEY)

'''
LLM Abstraction
'''
class LLM(ABC):

    def __init__(self, model: str) -> None:
        self.model = model

    @abstractmethod
    def get_message_history(self, conversation) -> list: pass

    @abstractmethod
    def __call__(self, system_prompt: str, user_prompt: str, conversation) -> Any: pass


class OpenAILLM(LLM):
    def __init__(self, model: str = 'gpt-4o-mini'):
        self.model = model
        super().__init__(model=model)

    def get_message_history(self, conversation):
        message_history = []
        
        for message in conversation.messages:
            message_history.append({ 'role': message['role'], 'content': [{ 'type': 'text', 'text': message['message'] }] })
        
        return message_history
    

    def __call__(
        self,
        system_prompt: str,
        user_prompt: str,
        conversation,
        stream: bool = False,
        temperature: float = 0.2,
        max_tokens: int = 1024
    ):
        messages = [] # NOTE: Adding conversation history in user prompt
        messages.insert(0, {'role': 'system', 'content': [{'type': 'text', 'text': system_prompt}]})
        next_message = {'role': 'user', 'content': [{'type': 'text', 'text': user_prompt}]}
        messages.append(next_message)

        kwargs = {}
        if stream:
            kwargs = { 'stream_options': {'include_usage': True} }

        response = openai_client.chat.completions.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=messages,
            stream=stream,
            **kwargs
        )
        
        if not stream:
            return response.choices[0].message.content

        return response


class Embedding():
    def __init__(self, model='text-embedding-3-small'):
        self.model = model

    def __call__(self, query: str):
        return openai_client.embeddings.create(model=self.model, input=query).data[0].embedding
