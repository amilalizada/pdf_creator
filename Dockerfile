FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade pip==21.2.4

RUN pip install -r requirements.txt 

RUN apt-get update && apt-get install -y libgl1-mesa-glx

COPY . /app

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port=80"]