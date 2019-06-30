FROM python:3.7.3-stretch

# System deps:
RUN apt update && apt -y upgrade
RUN pip3 install poetry

# Copy only requirements to cache them in docker layer
WORKDIR /textstats
COPY poetry.lock pyproject.toml /textstats/

# Project initialization:
RUN poetry config settings.virtualenvs.create false
RUN poetry install --no-interaction

# spacy models
RUN python -m spacy download nl_core_news_sm
# RUN python -m spacy download fr_core_news_md

# Creating folders, and files for a project:
COPY . /textstats/

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

ENV FLASK_APP textstats/main.py
EXPOSE 5000
CMD ["flask", "run"]
