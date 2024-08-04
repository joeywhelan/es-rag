import os
from dotenv import load_dotenv
from operator import itemgetter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain import hub
from langchain_core.runnables import RunnablePassthrough, RunnableParallel, Runnable
from langchain_core.output_parsers import StrOutputParser
from langchain_elasticsearch import ElasticsearchStore
import chainlit as cl
from esload import load

load_dotenv(override=True)
load()

def build_chain() -> Runnable:

    retriever = ElasticsearchStore(
        es_url="http://elasticsearch:9200",
        es_user="elastic",
        es_password="elastic",
        index_name=os.getenv('ELASTIC_INDEX'),
        embedding=OpenAIEmbeddings()
    ).as_retriever()
        
    chain: Runnable = (
        { 'chat_history': RunnablePassthrough(), 'input': RunnablePassthrough() }
        | hub.pull("joeywhelan/rephrase")
        | ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0)
        | StrOutputParser()
        | RunnableParallel({ 'question': RunnablePassthrough() })
        | { 'context': itemgetter('question') | retriever, 'question': itemgetter('question') }
        | hub.pull('rlm/rag-prompt')
        | ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0)
        | StrOutputParser()
    )
    return chain

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set('chain', build_chain())
    cl.user_session.set('chat_history', [])

@cl.on_message
async def on_message(question: cl.Message):
    chat_history: list[str] = cl.user_session.get('chat_history')
    chain: Runnable = cl.user_session.get('chain')
    content = await chain.ainvoke({'chat_history': chat_history, 'input': question.content})
    answer = cl.Message(content=content)
    await answer.send()
    chat_history.append((question.content, answer.content))
    del chat_history[:-10]  
    cl.user_session.set('chat_history', chat_history)