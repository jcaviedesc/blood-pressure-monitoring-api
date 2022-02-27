FROM python:3.10.2-slim

WORKDIR /src
ARG DATABASE_CONNECTION_URI=someting
ARG DATABASE_NAME=sometingx2
ARG GOOGLE_APPLICATION_CREDENTIALS=sometingx4

COPY ./requirements.txt /src/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt

COPY ./app /src/app
COPY ./config /src/config
COPY ./build-envfile /src
RUN echo ${DATABASE_CONNECTION_URI}
RUN ./build-envfile

EXPOSE 8000
# run container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
