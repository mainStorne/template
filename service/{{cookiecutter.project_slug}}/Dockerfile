FROM python:3.11-slim

COPY src src
COPY alembic.sh .
RUN chmod +x alembic.sh
WORKDIR /src
RUN pip install -r requirements.txt
ENTRYPOINT ["/alembic.sh"]
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "80", "--reload"]