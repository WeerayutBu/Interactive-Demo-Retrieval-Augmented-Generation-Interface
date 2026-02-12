from __future__ import annotations
from src.settings import settings
from core.retriever import Retriever

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Union

from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, BaseMessage

Message = Dict[str, str]
Query = Union[str, Sequence[Message]]


def to_lc_messages(q: Query) -> List[BaseMessage]:
    if isinstance(q, str):
        return [HumanMessage(content=q)]
    out: List[BaseMessage] = []
    for m in q:
        role = (m.get("role") or "").lower()
        content = m.get("content", "")
        if role == "system":
            out.append(SystemMessage(content=content))
        elif role in {"human", "user"}:
            out.append(HumanMessage(content=content))
        elif role in {"assistant", "ai"}:
            out.append(AIMessage(content=content))
        else:
            out.append(HumanMessage(content=content))
    return out

@dataclass
class BaseLLM:
    model: str = "gpt-4o-mini"
    temperature: float = 0.2
    max_tokens: Optional[int] = None
    timeout: float = 60.0

    def __post_init__(self) -> None:
        self.retriever = Retriever("base")
        self.llm = ChatOpenAI(
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            timeout=self.timeout,
            api_key=settings.OPENAI_API_KEY
        )
    def __call__(self, query, history) -> str:
        facts = self.retriever(query)
        messages = [
            {"role":"system","content":"Provide a concise answer based solely on the given facts. If they are irrelevant or insufficient, say \"I don't know.\""},
            {"role": "system", "content": "Context:\n" + "\n".join(map(str, facts))},
            *history,  # limit history
            {"role": "user", "content": query},
        ]

        out = self.llm.invoke(to_lc_messages(messages)).content

        return {"response": out, 'citations': [], "facts": facts}


class LLMs:
    """Simple factory/dispatcher for different LLM backends."""

    def __init__(self, method="base", **kwargs: Any) -> None:
        if method in ["base", "gpt-4o-mini"]:
            self.model = BaseLLM(**kwargs)
        else:
            raise ValueError(f"Unknown method: {method!r}. Implement it or use 'base'.")

    def __call__(self, query: Query, history) -> Any:
        return self.model(query, history)


def main() -> None:
    llm = LLMs()
    messages: List[Message] = [
        {"role": "system", "content": "Answer the question."},
        {"role": "human", "content": "Count number 1,2,3"},
        {"role": "assistant", "content": "1,2,3"}, 
        {"role": "human", "content": "what is the next number?"},
        {"role": "assistant", "content": "4"}, 
        {"role": "human", "content": "what is the next number?"}
    ]

    out = llm(messages)
    print(out)

if __name__ == "__main__":
    main()


