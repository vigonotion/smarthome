FROM python:3.8-alpine

ENV APP=/app

RUN mkdir -p $APP
WORKDIR $APP

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt $APP
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./ $APP
ENTRYPOINT ["python", "app.py"]
