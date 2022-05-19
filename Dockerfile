FROM rozari0/python:latest

WORKDIR /app

COPY . .

RUN pipenv install --system --deploy --ignore-pipfile

CMD ["python3","-m","bot"]
