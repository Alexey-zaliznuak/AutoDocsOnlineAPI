FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN sudo apt-get install libpq-dev
RUN pip install -r requirements.txt --no-cache-dir
RUN pip install gunicorn==20.1.0

# Copy project files
COPY . .

# Static move
RUN python manage.py collectstatic
RUN cp -r /app/collected_static/. /app/backend_static/static/

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "backend.wsgi"]
