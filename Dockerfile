FROM python:2.7
LABEL maintainer="Robert Zhang"

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 80
CMD python dialogue.py