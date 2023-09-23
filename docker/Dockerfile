FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONIOENCODING UTF-8

ARG UID="1000"
ARG GID="1000"
ARG USER="user"

WORKDIR /project/

COPY pyproject.toml poetry.lock /project/

RUN addgroup --gid $GID $USER && \
    adduser --uid $UID --gid $GID --disabled-password --gecos '' $USER && \
    usermod -aG sudo $USER && \
    echo "%sudo ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && \
    pip install --upgrade pip && \
    pip install poetry==1.6.1 certifi && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

COPY app /project/app
ADD docker/prod.env /project/app/.env

WORKDIR /project/

CMD ["python", "-m", "app"]
