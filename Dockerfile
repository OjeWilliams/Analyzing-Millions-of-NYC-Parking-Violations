FROM python:3.9

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

WORKDIR /app/src

ENTRYPOINT ["python", "main.py"]