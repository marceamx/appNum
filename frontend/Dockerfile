FROM python:3

LABEL maintainer="El viejo <marceamx@gmail.com>"

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY app.py .

ENTRYPOINT ["python", "app.py"]

