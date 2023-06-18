FROM python:latest
LABEL tag="backend"

COPY . /app
WORKDIR /app
EXPOSE 8000
ENTRYPOINT ["./entrypoint.sh"]

