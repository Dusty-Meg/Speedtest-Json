FROM python:3.9-alpine
COPY app/requirements.txt /app/requirements.txt
WORKDIR /app
RUN apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev libffi-dev openssl-dev python3-dev make build-base && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

EXPOSE 5000

COPY app/. /app

ENTRYPOINT ["python"]
CMD ["app.py"]