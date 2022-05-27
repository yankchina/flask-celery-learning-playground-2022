FROM python:3.7
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN apt-get update \
    && apt-get install -y --no-install-recommends
RUN pip install -r requirements.txt
COPY . /app