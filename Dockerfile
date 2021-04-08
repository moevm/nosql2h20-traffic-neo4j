FROM python:3.7-slim

RUN pip install --upgrade pip

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
ADD . /traffic
WORKDIR /traffic
EXPOSE 5000

CMD gunicorn manage:app -b 0.0.0.0:5000
