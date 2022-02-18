FROM python:3.10.2-slim

WORKDIR /src

COPY ./requirements.txt /src/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt

COPY ./app /src/app
# COPY ./config /src/config

EXPOSE 8000
# run container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
