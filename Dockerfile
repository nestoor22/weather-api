# base image
FROM python:3.11-slim-bookworm as base

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH .

COPY ./requirements.txt /code

RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir awscli-local[ver1]
RUN pip install --no-cache-dir -r /code/requirements.txt

FROM base as service

COPY . /code/

EXPOSE 8000

CMD ["sh", "/code/start.sh", "1"]
