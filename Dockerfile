FROM python:3.10.2-slim

WORKDIR /src
ENV DATABASE_CONNECTION_URI someting
ENV DATABASE_NAME sometingx2
ENV GOOGLE_APPLICATION_CREDENTIALS_PATH somewhere
ENV GOOGLE_APPLICATION_CREDENTIALS somewhere1

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
