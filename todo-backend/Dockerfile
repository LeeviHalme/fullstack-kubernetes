FROM python:3.13-slim

WORKDIR /usr/src/app

COPY poetry.lock pyproject.toml ./

RUN pip install poetry && poetry install

COPY . .

CMD ["poetry", "run", "python", "-u", "./main.py"]