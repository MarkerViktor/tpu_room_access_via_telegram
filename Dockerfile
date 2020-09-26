FROM python:3.8

RUN mkdir /room_access
WORKDIR /room_access

COPY /room_access /room_access

RUN pip install -r requirements.txt

CMD python /room_access/start.py