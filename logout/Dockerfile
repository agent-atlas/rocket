FROM python:3.8-slim-buster

WORKDIR /

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY autologout.py .

CMD ["python", "./autologout.py"]
