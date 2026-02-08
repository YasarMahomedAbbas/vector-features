FROM python:3.14

# Install GDAL dependencies and GDAL itself to enable GeoDjango support
RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /app

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/
EXPOSE 8000

# Wait for DB to start. Run migrations, create superuser (skip if already exists), then start server
CMD ["sh", "-c", "while ! python -c 'import socket; s=socket.create_connection((\"db\", 5432))' 2>/dev/null; do echo 'Waiting for db...'; sleep 1; done && python manage.py migrate && (python manage.py createsuperuser --noinput || true) && python manage.py runserver 0.0.0.0:8000"]


