# Dockerfile
FROM python:3.9
ENV POETRY_VIRTUALENVS_CREATE=false
WORKDIR /learn-english-bot
COPY . /learn-english-bot
# System deps:
RUN pip install "poetry==1.1.13"
RUN poetry install
EXPOSE 8000
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait
RUN chmod +x /wait
ENTRYPOINT ["./docker-entrypoint.sh"]
