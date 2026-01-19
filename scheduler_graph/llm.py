"""
A factory for creating LLM clients.
"""

import os

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI


llm_service_registry = {
    "OpenAI": lambda: ChatOpenAI(
        api_key=os.environ["OPENAI_API_KEY"],
        model_name=os.environ["OPENAI_MODEL"]
    )
}


def create_llm_client(service: str) -> BaseChatModel:
    """
    A provider-agnostic factory that returns an instance of a sub-class
    of the LangChain BaseChatModel.
    The specific service and its configuration are defined as environment
    variables via .env.
    """

    try:
        factory = llm_service_registry[service]
    except KeyError:
        raise ValueError(f"Unsupported LLM service: '{service}'.")

    return factory()
