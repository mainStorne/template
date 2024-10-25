FROM python:3.11-slim

COPY src app
COPY alembic.sh .
RUN chmod +x alembic.sh
WORKDIR /app
RUN pip install -r requirements.txt
WORKDIR /app/src
ENTRYPOINT ["/alembic.sh"]
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "80", "--reload"]