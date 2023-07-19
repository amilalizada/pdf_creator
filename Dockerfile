FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY requirements.txt requirements.txt

RUN pip install -U pip

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y \
    xvfb \
    fontconfig

RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.focal_amd64.deb \
    && dpkg -i  wkhtmltox_0.12.6-1.focal_amd64.deb \
    && apt-get install -f -y \
    && rm wkhtmltox_0.12.6-1.focal_amd64.deb

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

COPY . /app

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port=80"]
