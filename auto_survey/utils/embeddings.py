from langchain.embeddings import HuggingFaceEmbeddings
import os

openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key is not None:
    from langchain.embeddings.openai import OpenAIEmbeddings
    openai_embedding = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=openai_api_key)
else:
    openai_embedding = None

model_name = 'sentence-transformers/all-MiniLM-L6-v2'
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}

all_minilm_l6_v2 = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs)


EMBEDDINGS = {"text-embedding-ada-002": openai_embedding, "all-MiniLM-L6-v2": all_minilm_l6_v2}