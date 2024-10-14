FROM python:3.11-slim

# set working directory
WORKDIR /insurance-list-maker

# install poetry
RUN apt update && apt install -y git
RUN pip install poetry

# install project
ENV PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
COPY pyproject.toml .
COPY README.md .
RUN poetry install

# copy project
COPY app .
COPY database.csv.example database.csv

# expose port
EXPOSE 8501

# healthcheck
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# set entrypoint
ENTRYPOINT ["poetry", "run", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
