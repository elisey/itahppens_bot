FROM python:3.11

ENV PYTHONUNBUFFERED 1
ENV PYTHONIOENCODING UTF-8

ARG UID="1000"
ARG GID="1000"
ARG USER="user"

WORKDIR /project/

ADD pyproject.toml /project
ADD poetry.lock /project

RUN addgroup --gid $GID $USER && \
    adduser --uid $UID --gid $GID --disabled-password --gecos '' $USER && \
    usermod -aG sudo $USER && \
    echo "%sudo ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && \
    pip install --upgrade pip && \
    pip install poetry==1.1.13 certifi && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev && \
    mkdir /data

COPY bot /project/bot
ADD docker/prod.env /project/bot/.env

COPY docker/entrypoint.sh /project/bot/entrypoint.sh
RUN chmod +x /project/bot/entrypoint.sh

WORKDIR /project/bot

ENTRYPOINT ["/project/bot/entrypoint.sh"]
