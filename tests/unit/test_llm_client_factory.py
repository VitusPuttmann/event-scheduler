"""
Unit tests for the LLM client factory.
"""

import pytest

from langchain_openai import ChatOpenAI

from scheduler_graph.llm import create_llm_client


def test_create_llm_client_returns_chatopenai(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_MODEL", "test-model")

    llm_client = create_llm_client("OpenAI")

    assert isinstance(llm_client, ChatOpenAI)
    assert llm_client.model_name == "test-model"


def test_create_llm_client_raises_valueerror_for_unknown_service(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_MODEL", "test-model")

    with pytest.raises(ValueError) as err:
        llm_client = create_llm_client("NotAProvider")
    
    msg = str(err.value)

    assert "Unsupported LLM service" in msg
    assert "NotAProvider" in msg


def test_create_llm_client_raises_keyerror_for_missing_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setenv("OPENAI_MODEL", "test-model")

    with pytest.raises(KeyError):
        create_llm_client("OpenAI")
