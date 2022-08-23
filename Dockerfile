FROM python:3.10.2-slim

WORKDIR /src
ARG DATABASE_CONNECTION_URI ${DATABASE_CONNECTION_URI}
ARG DATABASE_NAME sometingx2
ARG GOOGLE_APPLICATION_CREDENTIALS path_to_file
ARG GOOGLE_APPLICATION_CREDENTIALS_FILE content

COPY ./requirements.txt /src/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt

COPY ./app /src/app
COPY ./pre-build /src

RUN mkdir -p /src/config
RUN ./pre-build

EXPOSE 8000
# run container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
