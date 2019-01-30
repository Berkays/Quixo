FROM python:3.6

WORKDIR /app

RUN python -m ensurepip
RUN python -m pip install numpy

COPY . .
CMD [ "python", "./play.py" ]