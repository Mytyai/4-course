FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY services.py .

ENV WEATHER_API_KEY=your_api_key_here

CMD ["python", "services.py"]

