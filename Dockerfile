FROM python:3.11-slim

WORKDIR /home/api/application

COPY requirements.txt /home/api/application

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 80

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]
# CMD ["pipenv", "run", "gunicorn", "src.main