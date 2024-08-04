FROM python:3.10-slim
WORKDIR /app
COPY ./.env ./
COPY ./requirements.txt ./
#RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install -qU python-dotenv langchain_elasticsearch bs4 langchain langchain_openai langchainhub chainlit
COPY ./app ./
EXPOSE 8000
CMD ["chainlit", "run" , "bot.py", "--host=0.0.0.0", "--port=8000"]