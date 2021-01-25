FROM python:3.6.9-slim-buster as build

COPY . /app/
WORKDIR /app/

RUN python -O -m compileall -q -f -b .
RUN tar cf /inventory_api.tar --exclude='*.py' --exclude=tests --exclude=.git .


FROM python:3.6.9-slim-buster

# Git commit hash that the image was built on
ARG BUILD_HASH
ENV BUILD_HASH=${BUILD_HASH}
# Git commit creation timestamp
ARG BUILD_TIMESTAMP
ENV BUILD_TIMESTAMP=${BUILD_TIMESTAMP}

EXPOSE 5000

WORKDIR /app
COPY requirements.txt /app/

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    apt-get install -y build-essential make gcc locales libffi-dev libpq-dev libevent-2.1.6 && \
    python -m pip install --no-cache-dir -r requirements.txt && \
    apt-get remove -y --purge make gcc build-essential libffi-dev && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

RUN DEBIAN_FRONTEND=noninteractive dpkg-reconfigure locales && \
    locale-gen C.UTF-8 && \
    /usr/sbin/update-locale LANG=C.UTF-8
ENV LC_ALL C.UTF-8

COPY --from=build /inventory_api.tar /app
RUN tar xf inventory_api.tar

CMD ["./run_api.sh"]
