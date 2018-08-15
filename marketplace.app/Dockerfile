FROM python:3.6
COPY marketplace/ /app/marketplace
COPY ./requirements.txt /app/
COPY ./runserver.py /app
RUN pip install -r app/requirements.txt
WORKDIR /app
ENV FLASK_APP=runserver.py
CMD flask run --port=8000 --host=0.0.0.0
