FROM python:3.13.3-slim

WORKDIR /app

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY src/main.py ./src/main.py
COPY src/client ./src/client
COPY src/configs ./src/configs
COPY src/parser ./src/parser
COPY src/routes ./src/routes

WORKDIR /app/src

EXPOSE 7000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7000"]
