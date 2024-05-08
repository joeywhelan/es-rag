# Elastic Demo
## Contents
1.  [Summary](#summary)
2.  [Features](#features)
3.  [Prerequisites](#prerequisites)
4.  [Installation](#installation)
5.  [Usage](#usage)

## Summary <a name="summary"></a>
This is a demo of usage of Elastic as a vector store for Retrieval Augmented Generation (RAG) for this scenario:
- Pure LangChain Expression Language (LCEL) chain with no safeguards on user or LLM interactions
Content from the Elastic online documentation of Elastic Vector Search is used for the RAG content.  

## Features <a name="features"></a>
- Elastic Search for the vector store
- Python Bot server (Chainlit)
- LangChain implementation of RAG with Elastic

## Prerequisites <a name="prerequisites"></a>
- Docker
- Docker Compose
- python3
- git
- pip

## Installation <a name="installation"></a>
```bash
git clone https://github.com/joeywhelan/es-rag.git && cd es-rag
pip install -qU python-dotenv langchain_elasticsearch bs4 langchain langchain_openai langchainhub chainlit
```
- Edit the .env_template file with your OpenAI key, Elastic Cloud ID, and Elastic Cloud API Key and rename the file to .env

## Usage <a name="usage"></a>
### Environment Start Up
```bash
python3 esload.py
chainlit run bot.py --host=0.0.0.0 --port=8000
```
