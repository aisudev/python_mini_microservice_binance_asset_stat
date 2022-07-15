FROM python:3.10-alpine3.15

WORKDIR /server
COPY . /server/
RUN pip install --upgrade pip
RUN pip install -r /server/requirements.txt

ENV PYTHONPATH=/server/

CMD sleep 10 && uvicorn rest.main:app --host 0.0.0.0 --port 80
