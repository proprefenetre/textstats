# Use Debian b/c of cython dependencies
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

# spacy model
RUN python -m spacy download nl_core_news_sm
RUN python -m spacy download fr_core_news_sm
RUN python -m spacy download en_core_web_sm

# Creating folders, and files for a project:
COPY . .

CMD [ "gunicorn", "-c", "gunicorn.py", "src:app" ]
