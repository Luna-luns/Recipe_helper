FROM python:3.8-slim
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r /app/requirements.txt --no-cache-dir
COPY . /app
CMD ["gunicorn", "api_foodgram.wsgi:application", "--bind", "0:8000"]
