# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0

import os
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from config.config import LLM_PROVIDER

def get_llm():
    """
    Get the LLM provider based on the configuration.
    Supports: openai, anthropic, azure-openai, groq
    """
    provider = LLM_PROVIDER.lower()
    
    if provider == "openai":
        return ChatOpenAI(
            model=os.getenv("OPENAI_MODEL_NAME", "gpt-4o"),
            temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.7")),
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_ENDPOINT", "https://api.openai.com/v1"),
        )
    elif provider == "anthropic":
        return ChatAnthropic(
            model=os.getenv("ANTHROPIC_MODEL_NAME", "claude-3-5-sonnet-20241022"),
            temperature=float(os.getenv("ANTHROPIC_TEMPERATURE", "0.7")),
            api_key=os.getenv("ANTHROPIC_API_KEY"),
        )
    elif provider == "azure-openai":
        from langchain_openai import AzureChatOpenAI
        return AzureChatOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2023-12-01-preview"),
            temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.7")),
        )
    elif provider == "groq":
        from langchain_groq import ChatGroq
        return ChatGroq(
            model=os.getenv("GROQ_MODEL_NAME", "llama-3.3-70b-versatile"),
            api_key=os.getenv("GROQ_API_KEY"),
            temperature=float(os.getenv("GROQ_TEMPERATURE", "0.7")),
        )
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")
