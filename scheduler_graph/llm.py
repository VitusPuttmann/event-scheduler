"""
Define class for LLM requests.
"""

import os
from typing import List

from langchain_openai import ChatOpenAI

from models.event import Event


class LLMClientOpenAI():
    def __init__(self, api_key: str):
        self.client = ChatOpenAI(api_key=api_key, model_name="gpt-4o-mini")
    
    def query(
            self, system_message: str, query_message: str, context: str | dict[str, List[Event]]
        ) -> str:
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": query_message},
            {"role": "user", "content": f"Context:\n{context}"}
        ]
        response = self.client.invoke(messages)
        
        return response.content


class LLMClient():
    """
    General client for conducting LLM requests. Specific service defined as
    environment variable.
    """

    service_registry = {
        "OpenAI": lambda: LLMClientOpenAI(api_key=os.environ["OPENAI_API_KEY"])
    }

    def __init__(self, service: str):
        self.client = self.service_registry[service]()

    def query(
            self, system_message: str, query_message: str, context: str | dict[str, List[Event]]
        ) -> str:
        
        response = self.client.query(system_message, query_message, context)

        return response
