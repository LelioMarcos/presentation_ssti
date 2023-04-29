# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

RUN mkdir -p /app

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD ["python3", "-m" , "flask", "--app", "server", "--debug", "run", "--host=0.0.0.0"]
