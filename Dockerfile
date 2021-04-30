FROM python:3

ENV DEBIAN_FRONTEND=noninteractive

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt


ENTRYPOINT ["python","/app/main.py"]