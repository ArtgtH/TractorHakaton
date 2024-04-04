FROM python:3.11-slim

WORKDIR /st-app

EXPOSE 8501

COPY requirements.txt requirements.txt

RUN apt-get update && pip install -r requirements.txt

COPY . .

RUN rm ./requirements.txt

CMD ["streamlit", "run", "auth.py"]
