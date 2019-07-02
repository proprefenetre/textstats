FROM python:3.7.3-stretch

# System deps:
RUN apt update && apt -y upgrade
RUN pip3 install poetry

# Copy only requirements to cache them in docker layer
WORKDIR /app
COPY poetry.lock pyproject.toml /app/

# Project initialization:
RUN poetry config settings.virtualenvs.create false
RUN poetry install --no-interaction

# spacy model
RUN python -m spacy download nl_core_news_sm

# Creating folders, and files for a project:
COPY . .

ENV FLASK_APP=textstats
ENV FLASK_ENV=development

CMD [ "gunicorn", "-c", "gunicorn.py", "src:app" ]
