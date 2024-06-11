FROM ubuntu:latest

RUN apt update

RUN apt install -y python3 python3-pip 

COPY main.py /

COPY db.py /

COPY auth.py /

COPY config.py / 

COPY models.py /

COPY requirements.txt / 

RUN python3 -m pip install -r requirements.txt

CMD ["uvicorn", "--host=0.0.0.0", "--port=8000", "main:app"]