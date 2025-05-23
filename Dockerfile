# --------- requirements ---------

FROM python:3.13 AS requirements-stage

WORKDIR /tmp

RUN pip install uv

COPY ./pyproject.toml ./uv.lock* /tmp/

RUN uv export --no-hashes --format requirements-txt > requirements.txt


FROM python:3.13

WORKDIR /code

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app
COPY ./migrations /code/migrations
COPY ./alembic.ini /code


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]