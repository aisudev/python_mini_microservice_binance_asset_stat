FROM python:3.10-alpine3.15

WORKDIR /binance
COPY . /binance/
RUN apk add build-base
RUN pip install --upgrade pip
RUN pip install -r /binance/requirements.txt

ENV PYTHONPATH=/binance/

CMD sleep 10 && python main.py