FROM python3.10.6:slim-buster

WORKDIR /app

COPY . .

RUN pip3 install -U -r requirements.txt

CMD ["python3","-m","bot"]
