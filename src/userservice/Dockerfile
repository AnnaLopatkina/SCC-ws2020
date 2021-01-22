FROM python:3.8

RUN pip install pipenv

WORKDIR .

COPY . .

RUN pipenv install

ENV FLASK_APP app.py

CMD [ "pipenv", "run", "gunicorn", "-w", "4", "-b", ":5001", "app:app" ]
