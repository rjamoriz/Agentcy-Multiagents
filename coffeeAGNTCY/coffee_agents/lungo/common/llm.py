# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0

import os
from config.config import LLM_PROVIDER

def get_llm():
    """
    Get the LLM provider based on the configuration.
    """
    provider = LLM_PROVIDER.lower()
    
    if provider == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            model=os.getenv("OPENAI_MODEL_NAME", "gpt-4o"),
            temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.7")),
        )
    elif provider == "anthropic":
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY"),
            model=os.getenv("ANTHROPIC_MODEL_NAME", "claude-3-5-sonnet-20241022"),
            temperature=float(os.getenv("ANTHROPIC_TEMPERATURE", "0.7")),
        )
    elif provider == "azure-openai":
        from langchain_openai import AzureChatOpenAI
        return AzureChatOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2023-12-01-preview"),
            temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.7")),
        )
    elif provider == "groq":
        from langchain_groq import ChatGroq
        return ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model=os.getenv("GROQ_MODEL_NAME", "llama-3.3-70b-versatile"),
            temperature=float(os.getenv("GROQ_TEMPERATURE", "0.7")),
        )
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")
