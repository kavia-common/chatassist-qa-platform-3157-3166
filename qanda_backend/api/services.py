import os
from typing import List, Tuple

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI


class OpenAIChatService:
    """
    Encapsulates LangChain + OpenAI chat functionality.
    """

    def __init__(self, model: str | None = None, temperature: float = 0.2):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY environment variable is not set. Please configure it in the environment.")
        self.model_name = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        # ChatOpenAI picks up the API key from env automatically
        self.llm = ChatOpenAI(model=self.model_name, temperature=temperature)

    def build_history(self, messages: List[Tuple[str, str]]):
        """
        Build LangChain messages from (role, content).
        """
        lc_messages = []
        for role, content in messages:
            if role == "user":
                lc_messages.append(HumanMessage(content=content))
            elif role == "assistant":
                lc_messages.append(AIMessage(content=content))
            elif role == "system":
                lc_messages.append(SystemMessage(content=content))
        return lc_messages

    # PUBLIC_INTERFACE
    def generate_reply(self, history: List[Tuple[str, str]], prompt: str) -> str:
        """Generate an assistant reply using prior history and the new prompt."""
        lc_messages = self.build_history(history)
        lc_messages.append(HumanMessage(content=prompt))
        result = self.llm.invoke(lc_messages)
        # result is AIMessage
        return result.content if hasattr(result, "content") else str(result)
