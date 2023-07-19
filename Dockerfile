FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY requirements.txt requirements.txt

RUN pip install -U pip

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y \
    xvfb \
    fontconfig

RUN apt-get update

RUN wget http://archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2_amd64.deb \
    && dpkg -i libssl1.1_1.1.1f-1ubuntu2_amd64.deb \
    && rm libssl1.1_1.1.1f-1ubuntu2_amd64.deb

RUN wget https://netix.dl.sourceforge.net/project/libjpeg-turbo/2.0.5/libjpeg-turbo-official_2.0.5_amd64.deb \
    && dpkg -i libjpeg-turbo-official_2.0.5_amd64.deb \
    && rm libjpeg-turbo-official_2.0.5_amd64.deb

RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.focal_amd64.deb \
    && dpkg -i  wkhtmltox_0.12.6-1.focal_amd64.deb \
    && apt-get install -f -y \
    && rm wkhtmltox_0.12.6-1.focal_amd64.deb

COPY . /app

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port=80"]
