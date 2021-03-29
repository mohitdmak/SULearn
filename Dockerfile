FROM python:latest

WORKDIR /coursera

COPY . .

RUN pip3 install -r req.txt

RUN python3 manage.py makemigrations

RUN python3 manage.py migrate

CMD ["python3","manage.py", "runserver", "0.0.0.0:8000"]

