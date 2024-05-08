import os
from bs4 import SoupStrainer
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_elasticsearch import ElasticsearchStore


ES_DOC_URLS=[
    "https://www.elastic.co/guide/en/elasticsearch/reference/8.13/knn-search.html",
    "https://www.elastic.co/search-labs/blog/how-to-deploy-nlp-text-embeddings-and-vector-search",
    "https://www.elastic.co/search-labs/blog/vector-search-elasticsearch-rationale"
]

load_dotenv(override=True)

def get_docs():
    loader = WebBaseLoader(
        web_paths=ES_DOC_URLS,
        bs_kwargs={'parse_only': SoupStrainer(['p'])}
    )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=20,
        length_function=len,
        is_separator_regex=False
    )
    return loader.load_and_split(splitter)

def load():
    evs = ElasticsearchStore.from_documents(
        documents=get_docs(),
        es_cloud_id=os.getenv('ELASTIC_CLOUD_ID'),
        es_api_key=os.getenv('ELASTIC_API_KEY'),
        index_name=os.getenv('ELASTIC_INDEX'),
        embedding=OpenAIEmbeddings()
    )

if __name__ == '__main__':
    load()