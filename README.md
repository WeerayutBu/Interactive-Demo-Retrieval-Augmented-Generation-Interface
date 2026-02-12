# Interactive Demo: Retrieval-Augmented Generation (RAG) Interface

This demo built with **FastAPI** and **Streamlit**. FastAPI provides chat and RAG APIs, while Streamlit offers a simple user interface. The system uses the **GPT API** as the LLM and a **local API retriever** to ground responses in retrieved context.

- GPT API as the LLM  
- FastAPI for chat, search, and RAG APIs  
- Streamlit for a simple UI  
- Local API retriever for contextual grounding  

![RAG Interface Demo](images/demo.png)

## Requirements

- Python **3.10** +
- GPT / OpenAI API key


## Setup

```bash
pip install -r requirements.txt
```

## Run FAST API (Chat and Rag)
```python 
python -m uvicorn api.main:app --reload
```

## Run steamlit
```python
streamlit run ui/main.py 
```


Create a .env file:
```bash
OPENAI_API_KEY=your_api_key
```

## Project Structure

```text
.
├── api/
│   ├── routes/
│   │   ├── chat.py        # Chat endpoints
│   │   ├── rag.py         # RAG endpoints
│   │   └── search.py      # Retrieval endpoints
│   └── main.py            # FastAPI app entry
│
├── core/
│   ├── llm.py             # GPT / Local LLMs
│   └── retriever.py       # API / Local retriever
│
├── ui/
│   ├── display.py         
│   ├── main.py            # Streamlit entry
│   └── utils.py           
│
├── .env                   # Environment variables
├── requirements.txt
└── README.md
```

## Note
- Demo / learning project
- Easily extendable with vector databases (FAISS, Chroma, etc.)

