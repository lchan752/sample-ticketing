FROM debian:8.7

# need libssl-dev for pip install cryptography
# need libpq-dev for pip install psycopg2
RUN apt-get update && apt-get install -y \
	python3 \
	python3-dev \
	python3-setuptools \
	python3-pip \
	virtualenv \
	libpq-dev \
	pkg-config \
	postgresql-client \
	build-essential
RUN virtualenv /venv/ -p `which python3`
RUN /venv/bin/pip install --upgrade --force-reinstall pip setuptools

ENV LANG C.UTF-8

COPY requirements.txt /app/requirements.txt
RUN /venv/bin/pip install -r /app/requirements.txt

COPY . /app/
WORKDIR /app/

EXPOSE 80

CMD ["/venv/bin/daphne", "-b", "0.0.0.0", "-p", "80", "ticketing.asgi:channel_layer"]
