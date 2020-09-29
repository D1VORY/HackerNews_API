# pull official base image
FROM python:3.8


#update
# Install Ubuntu dependencies
RUN apt-get update
#    && apk add --virtual build-deps gcc g++ python3-dev musl-dev \
#    && apk add postgresql-dev \
#    && apk del build-deps

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE 1

# set work directory
RUN mkdir /app
WORKDIR /app

COPY ./requirements.txt /app/
COPY ./.env /app/dashboard/dashboard/
COPY ./.env /app/dashboard/

RUN pip install -r requirements.txt

COPY . /app/

#create non root user
#RUN adduser -D olexandr
#USER olexandr


# run gunicorn
CMD gunicorn dashboard.wsgi:application --bind 0.0.0.0:$PORT
