


# FROM python:alpine3.7
# COPY ./requirements.txt /app/requirements.txt
# WORKDIR /app
# RUN apk --update add python py-pip openssl ca-certificates py-openssl wget
# RUN apk --update add --virtual build-dependencies libffi-dev openssl-dev python-dev py-pip build-base
# RUN pip install -r requirements.txt
# COPY . /app
# EXPOSE 5000
# ENTRYPOINT [ "python3", "app.py" ]

FROM python:3.7
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN apt-get update \
    && apt-get install -y --no-install-recommends
RUN pip install -r requirements.txt
COPY . /app
EXPOSE 5000
# ENTRYPOINT [ "python3", "app.py" ]
# ENTRYPOINT ["gunicorn","--bind","0.0.0.0:5000","-k","geventwebsocket.gunicorn.workers.GeventWebSocketWorker","-w","1","wsgi:app"]


