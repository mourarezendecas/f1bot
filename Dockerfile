FROM python:3.9.23-trixie

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY *.py ./

CMD ["python3", "main.py"]