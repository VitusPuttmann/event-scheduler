"""
Define class for LLM requests.
"""

import json
import os
from typing import Any

from langchain_openai import ChatOpenAI


class LLMClientOpenAI():
    def __init__(self, api_key: str):
        self.client = ChatOpenAI(api_key=api_key, model_name="gpt-4o-mini")
    
    def query(
            self, system_message: str, query_message: str, context: dict[str, Any]
        ) -> str:
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": query_message},
            {"role": "user", "content": f"Context:\n{json.dumps(context, ensure_ascii=False)}"}
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
            self, system_message: str, query_message: str, context: dict[str, Any]
        ) -> str:
        
        response = self.client.query(system_message, query_message, context)

        return response
