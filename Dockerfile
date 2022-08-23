FROM python:3.10.2-slim

WORKDIR /src
ARG DATABASE_CONNECTION_URI ${DATABASE_CONNECTION_URI}
ARG DATABASE_NAME sometingx2
ARG GOOGLE_APPLICATION_CREDENTIALS_PATH somewhere
ARG GOOGLE_APPLICATION_CREDENTIALS somewhere1

RUN echo "GOOGLE_APPLICATION_CREDENTIALS_PATH = ${GOOGLE_APPLICATION_CREDENTIALS_PATH}"
COPY ./requirements.txt /src/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt

COPY ./app /src/app
COPY ./pre-build /src

RUN mkdir -p /src/config
RUN echo ${DATABASE_CONNECTION_URI}
RUN ./pre-build

EXPOSE 8000
# run container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
