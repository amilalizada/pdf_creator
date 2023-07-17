FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY requirements.txt requirements.txt

RUN apt-get install -y build-essential libssl-dev libffi-dev python3-dev

RUN pip install --upgrade pip==21.2.4

RUN pip install -r requirements.txt 

RUN apt-get update && apt-get install -y libgl1-mesa-glx

COPY . /app

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port=80"]