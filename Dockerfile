FROM python:3.11.4-slim-bookworm AS base

ENV PATH=/usr/local/bin:$PATH
ENV PYTHONPATH=/app
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    gcc libffi-dev curl build-essential \
    && curl -sSL https://install.python-poetry.org | python3 - --version 1.8.4 \
    && ln -s /root/.local/bin/poetry /usr/local/bin/poetry \
    && apt-get remove -y gcc build-essential \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml poetry.lock /app/
RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-cache

COPY . /app
RUN chmod +x start.sh

FROM python:3.11.4-slim-bookworm AS final

WORKDIR /app
ENV PYTHONPATH=/app

COPY --from=base /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=base /usr/local/bin /usr/local/bin
COPY --from=base /app /app

RUN mkdir -p /app/logs

ENTRYPOINT ["sh", "start.sh"]
