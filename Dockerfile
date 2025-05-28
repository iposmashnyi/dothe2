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

COPY ./src/app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]