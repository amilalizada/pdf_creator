FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY requirements.txt .

RUN pip install -U pip
RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y \
    xvfb \
    fontconfig \
    xfonts-75dpi

RUN wget http://archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2_amd64.deb \
    && dpkg -i libssl1.1_1.1.1f-1ubuntu2_amd64.deb \
    && rm libssl1.1_1.1.1f-1ubuntu2_amd64.deb

RUN wget http://archive.ubuntu.com/ubuntu/pool/main/libj/libjpeg-turbo/libjpeg-turbo8_2.0.3-0ubuntu1.20.04.3_amd64.deb \
    && apt-get install -f -y \
    && dpkg -i libjpeg-turbo8_2.0.3-0ubuntu1.20.04.3_amd64.deb \
    && rm libjpeg-turbo8_2.0.3-0ubuntu1.20.04.3_amd64.deb

# RUN wget http://archive.ubuntu.com/ubuntu/pool/main/x/xfonts-75dpi/xfonts-75dpi_1.0.3_all.deb \
#     && dpkg -i xfonts-75dpi_1.0.3_all.deb \

RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.focal_amd64.deb \
    && dpkg -i  wkhtmltox_0.12.6-1.focal_amd64.deb \
    && apt-get install -f -y 

COPY . /app

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port=80"]

