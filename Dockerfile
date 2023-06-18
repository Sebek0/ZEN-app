FROM python:latest
LABEL tag="backend"

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "zen_api.main:app", "--host", "0.0.0.0"]
