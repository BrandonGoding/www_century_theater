# syntax=docker/dockerfile:1
FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements-production.txt /code/requirements.txt
RUN pip install -r requirements.txt
COPY www_century_theater /code/
RUN rm /code/www_century_theater/settings.py
RUN rm /code/www_century_theater/production_settings.py
#RUN rm -r /code/website/static

COPY www_century_theater/www_century_theater/production_settings.py /code/www_century_theater/settings.py
COPY production.env /code/.env
#COPY venv/lib/python3.9/site-packages/wagtailmenus/migrations /usr/local/lib/python3.10/site-packages/wagtailmenus/migrations

CMD [ "python", "manage.py", "runserver","0.0.0.0:80" ]