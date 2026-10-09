FROM python:3.12.0-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY src/mysite mysite

EXPOSE 8000

CMD ["uvicorn", "mysite.main:app", "--host", "0.0.0.0", "--port", "8000"]