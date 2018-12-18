FROM python:3.7.1

WORKDIR /usr/src/app
#ENV PYTHONPATH /usr/src/app
#COPY requirements.txt ./
#RUN pip install --no-cache-dir -r requirements.txt

COPY . .