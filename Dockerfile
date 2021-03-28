FROM ubuntu:18.04
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD python /app/app.py
