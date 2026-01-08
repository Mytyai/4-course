FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV WEATHER_API_KEY=your_api_key_here

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "weather_service.app:app"]
