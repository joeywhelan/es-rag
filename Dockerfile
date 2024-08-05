FROM python:3.10-slim
WORKDIR /app
COPY ./.env ./
RUN pip install -qU python-dotenv langchain_elasticsearch bs4 langchain langchain_openai langchainhub chainlit langchain_community
COPY ./app ./
EXPOSE 8000
CMD ["chainlit", "run" , "bot.py", "--host=0.0.0.0", "--port=8000"]