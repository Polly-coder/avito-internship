FROM python:3.12-slim

RUN apt-get -y update \
    && apt-get install -y postgresql postgresql-contrib gcc python3-dev musl-dev \
    # Cleanup apt cache
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/backend

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POSTGRES_DATABASE=postgres10
ENV POSTGRES_USERNAME=postgres
ENV POSTGRES_PASSWORD=postgres123
ENV POSTGRES_HOST=host.docker.internal
ENV POSTGRES_PORT=5433

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
#CMD ["python", "manage.py", "runserver"]
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
ENTRYPOINT ["/usr/src/backend/entrypoint.prod.sh"]
#CMD ["python", "manage.py", "runserver", "127.0.0.1:8000"]
