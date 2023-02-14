FROM python:3.10

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

COPY . .

RUN pip --no-cache-dir install -r requirements.txt

EXPOSE 8000

CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000