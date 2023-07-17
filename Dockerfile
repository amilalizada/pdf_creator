# FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# COPY requirements.txt requirements.txt

# RUN pip install -U pip

# RUN pip install -r requirements.txt 

# COPY . /app

# CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port=80"]
FROM python:3.9

WORKDIR /code

COPY requirements.txt requirements.txt

RUN pip install -U pip

COPY . /app

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port=80"]