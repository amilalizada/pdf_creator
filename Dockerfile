FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY requirements.txt requirements.txt

RUN pip install -U pip

RUN pip install -r requirements.txt 

COPY . /app