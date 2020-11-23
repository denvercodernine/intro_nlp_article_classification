FROM python:3.6-slim-buster
WORKDIR /app

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /app/app
EXPOSE 5000
COPY . .
CMD ["flask", "run"]