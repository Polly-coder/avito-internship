FROM python:3.12-slim

RUN apt-get -y update \
    && apt-get install -y postgresql postgresql-contrib gcc python3-dev musl-dev \
    # Cleanup apt cache
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/backend

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
#CMD ["python", "manage.py", "runserver", "127.0.0.1:8000"]
