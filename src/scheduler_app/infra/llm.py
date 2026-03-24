"""
Factory for creating LLM clients and token counter.
"""

import os

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI


llm_service_registry = {
    "OpenAI": {
        "llm_client": lambda: ChatOpenAI(
            api_key=os.environ["OPENAI_API_KEY"],
            model_name=os.environ["OPENAI_MODEL"]
        ),
        "input_token_field": "prompt_tokens",
        "output_token_field": "completion_tokens",
        "input_cost_env": "OPENAI_INPUT_COST_PER_M",
        "output_cost_env": "OPENAI_OUTPUT_COST_PER_M"
    }
}


class TokenCounter(BaseCallbackHandler):
    def __init__(self, service, dollars_already_spent, budget_exceeded):
        self.service = service
        self.input_token_field = (
            llm_service_registry[self.service]["input_token_field"]
        )
        self.output_token_field = (
            llm_service_registry[self.service]["output_token_field"]
        )
        self.input_token_cost = (
            float(os.environ[llm_service_registry[service]["input_cost_env"]]) / 1e6
        )
        self.output_token_cost = (
            float(os.environ[llm_service_registry[service]["output_cost_env"]]) / 1e6
        )
        self.dollars_spent_this_node = 0.0
        self.dollars_already_spent = dollars_already_spent
        self.budget_limit = float(os.environ["BUDGET_LIMIT"])
        self.budget_exceeded = budget_exceeded

    def on_llm_end(self, response, **kwargs):
        usage = response.llm_output.get("token_usage", {})

        expended = (
            (
                usage.get(self.input_token_field, 0) *
                self.input_token_cost
            ) +
            (
                usage.get(self.output_token_field, 0) *
                self.output_token_cost
            )
        )
        self.dollars_spent_this_node += expended

        if self.dollars_already_spent + self.dollars_spent_this_node >= self.budget_limit:
            self.budget_exceeded = True


def create_llm_client(
        service: str,
        dollars_already_spent: float,
        budget_exceeded: bool
    ) -> tuple[BaseChatModel, TokenCounter]:
    """
    A provider-agnostic factory that returns an instance of a sub-class
    of the LangChain BaseChatModel and an instance of TokenCounter.
    The specific service and its configuration are defined as environment
    variables via .env.
    """

    try:
        factory = llm_service_registry[service]["llm_client"]
    except KeyError:
        raise ValueError(f"Unsupported LLM service: '{service}'.")    

    token_counter = TokenCounter(service, dollars_already_spent, budget_exceeded)

    return factory(), token_counter
