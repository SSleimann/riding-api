FROM python:3.11.3-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Translations dependencies
  && apt-get install -y gettext \
  #geo
  && apt-get install -y binutils libproj-dev gdal-bin \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./compose/local/django/entrypoint entrypoint
RUN chmod +x entrypoint 

COPY ./compose/local/django/start start
RUN chmod +x start 

COPY ./compose/local/django/celery/beat/start start_celery_beat
RUN chmod +x start_celery_beat 

COPY ./compose/local/django/celery/worker/start start_celery_worker
RUN chmod +x start_celery_worker

COPY . .

ENTRYPOINT [ "./entrypoint" ]