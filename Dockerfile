FROM python:3.8-slim-bullseye

RUN apt update -y && apt upgrade -y

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python3", "-OO" ,"main.py"]