FROM python:3.6
COPY ./requirements.txt /app/
RUN pip install -r app/requirements.txt
COPY marketplace/ /app/marketplace
COPY ./runserver.py /app
WORKDIR /app
ENV FLASK_APP=runserver.py
# ARG CELERY_BROKER_URL
# ARG SQLALCHEMY_DATABASE_URI
