from dotenv import load_dotenv
import os

from langchain_openai import OpenAIEmbeddings
from langchain_elasticsearch import ElasticsearchStore

load_dotenv(override=True)
question = "What does a k-nearest neighbor search do?"

retriever = ElasticsearchStore(
        es_cloud_id=os.getenv('ELASTIC_CLOUD_ID'),
        es_api_key=os.getenv('ELASTIC_API_KEY'),
        index_name='rag_demo',
        embedding=OpenAIEmbeddings()
).as_retriever()

rag_context = retriever.invoke(question)
relevant_chunks = "\n".join([doc.page_content for doc in rag_context])
print(relevant_chunks)