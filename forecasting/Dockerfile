FROM python:3.11-slim

WORKDIR /api

EXPOSE 5555

COPY requirements.txt requirements.txt

RUN apt-get update && pip install -r requirements.txt

COPY . .

RUN rm ./requirements.txt

CMD ["flask", "--app", "app.py", "run", "-h", "0.0.0.0", "-p", "5555"]
