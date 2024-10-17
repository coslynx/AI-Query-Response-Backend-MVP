FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DATABASE_URL=postgresql://user:password@host:port/database
ENV OPENAI_API_KEY=YOUR_OPENAI_API_KEY
ENV JWT_SECRET_KEY=YOUR_JWT_SECRET_KEY

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]