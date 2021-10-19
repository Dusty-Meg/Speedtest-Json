FROM python:3.9-alpine
COPY app/requirements.txt /app/requirements.txt
WORKDIR /app
RUN apk update && \
 apk add --no-cache --virtual .build-deps gcc musl-dev libffi-dev openssl-dev python3-dev make build-base && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

RUN adduser -D speedtest

RUN export ARCHITECTURE=$(uname -m) && \
    if [ "$ARCHITECTURE" == 'armv7l' ]; then export ARCHITECTURE=arm; fi && \
    wget -O /tmp/speedtest.tgz "https://install.speedtest.net/app/cli/ookla-speedtest-1.0.0-${ARCHITECTURE}-linux.tgz" && \
    tar zxvf /tmp/speedtest.tgz -C /tmp && \
    cp /tmp/speedtest /usr/local/bin

EXPOSE 5000

COPY app/. /app

RUN chown -R speedtest:speedtest /app

USER speedtest

ENTRYPOINT ["python"]
CMD ["app.py"]