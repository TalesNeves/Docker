FROM python:3.8.5-alpine
RUN set -e; \
        apk add --no-cache --virtual .build-deps \
                gcc \
                libc-dev \
                linux-headers \
                mariadb-dev \
                python3-dev \
                postgresql-dev \
        ;

WORKDIR /app
ADD . /app/


RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev cargo
RUN pip install cffi
RUN pip install -r requirements.txt


CMD ["python","app.py"]
