FROM python:3.10-slim-buster
LABEL maintainer="genas.ng"

COPY ../requirements.txt /requirements.txt

COPY .. /app
WORKDIR /app

# Create virtual evn called /py
RUN python -m venv /py && \
    # Install requirements in virtual env /py
    /py/bin/pip install -r /requirements.txt && \
    adduser --disabled-password --no-create-home django-user

ENV PATH="/py/bin:$PATH"

USER django-user
