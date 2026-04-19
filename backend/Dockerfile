FROM python:3.11-slim

WORKDIR /app

RUN pip install uv

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app

USER appuser

COPY --chown=appuser:appuser pyproject.toml uv.lock ./
RUN uv sync --frozen && \
    uv pip install --python .venv/bin/python setuptools && \
    .venv/bin/python -c "import nltk; nltk.download('punkt_tab'); nltk.download('stopwords')"

COPY --chown=appuser:appuser . .

EXPOSE 8000
CMD ["sh", "-c", ".venv/bin/alembic upgrade head && .venv/bin/fastapi dev --port 8000 --host 0.0.0.0"]