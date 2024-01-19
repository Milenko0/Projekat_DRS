FROM python:3-alpine3.15
WORKDIR /app
COPY . /app
RUN pip install -r requiraments.txt
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]