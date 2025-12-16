FROM python:3.13-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

EXPOSE 5500

CMD ["gunicorn", "--bind", "0.0.0.0:5500", "main:app"]