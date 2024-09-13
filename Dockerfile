FROM python:3.12-slim

RUN apt-get -y update \
    && apt-get install -y postgresql postgresql-contrib gcc python3-dev musl-dev \
    # Cleanup apt cache
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/backend

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POSTGRES_DATABASE=cnrprod1725771832-team-78752
ENV POSTGRES_USERNAME=cnrprod1725771832-team-78752
ENV POSTGRES_PASSWORD=cnrprod1725771832-team-78752
ENV POSTGRES_HOST=rc1b-5xmqy6bq501kls4m.mdb.yandexcloud.net
ENV POSTGRES_PORT=6432
ENV target_session_attrs=read-write

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080
#CMD ["python", "manage.py", "runserver"]
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
ENTRYPOINT ["/usr/src/backend/entrypoint.prod.sh"]
