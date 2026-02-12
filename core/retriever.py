import json
import requests
from src.settings import settings

class BaseRetriever:
    def __init__(self, top_k=8, url=settings.VECTOR_DB_API_IP, token_id=settings.VECTOR_DB_API_KEY):
        self.url = url
        self.top_k = top_k
        self.headers = {'Authorization': token_id, 'Content-Type': 'application/json'}

    def __call__(self, query):
        payload = json.dumps({"query": query, "rerank": True})
        response = requests.request("POST", self.url, headers=self.headers, data=payload)
        response = json.loads(response.text)
        response = [r['content'] for r in response['facts']][:self.top_k]
        return response
    

class Retriever:
    def __init__(self, method="base", **kwargs):
        if method == "base":
            self.retriever = BaseRetriever(**kwargs)
        else:
            raise TypeError(f"Implement {method}")

    def __call__(self, query):
        return self.retriever(query)
    

if "__main__" == __name__:
    re = Retriever()
    out = re('สวัสดี')
    breakpoint()