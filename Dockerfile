FROM python:3.12.4-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y postgresql-client libpq-dev gcc \
    && apt-get clean

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]