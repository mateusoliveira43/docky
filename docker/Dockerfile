FROM mateusoliveira43/poetry:1.1-python3.10-slim

ARG GROUP_ID=1000
ARG USER_ID=1000
ARG USER_NAME=develop
ARG WORK_DIR=/home/$USER_NAME/PROJECT

RUN groupadd --gid $GROUP_ID $USER_NAME \
    && useradd --uid $USER_ID --gid $GROUP_ID --create-home $USER_NAME \
    && runuser --user $USER_NAME -- mkdir $WORK_DIR
USER $USER_NAME

WORKDIR $WORK_DIR
COPY pyproject.toml poetry.lock ./
RUN poetry install
