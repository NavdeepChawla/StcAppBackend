FROM ubuntu:20.04
COPY . /app
WORKDIR /app
RUN apt-get update
RUN apt-get install -y python3-pip
RUN pip3 install -r requirements.txt
CMD python /app/app.py
