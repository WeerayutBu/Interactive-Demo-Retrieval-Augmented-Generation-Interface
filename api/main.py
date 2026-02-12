from fastapi import FastAPI

from api.routes.rag import router as rag_router
from api.routes.chat import router as conv_router
from api.routes.search import router as search_router

from core.llm import LLMs
from core.retriever import Retriever

app = FastAPI()
app.include_router(search_router) # /search
app.include_router(conv_router) # /chat

@app.on_event("startup")
def startup():
    app.state.llms = {}
    app.state.llms['gpt-4o-mini'] = LLMs("gpt-4o-mini")
    app.state.retriever = Retriever("base")

app.include_router(rag_router) # /rag

@app.get("/")
def read_root():
    return "Hello!!!"

