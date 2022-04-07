FROM python:3.8-slim-buster
RUN mkdir /pdf && chmod 777 /pdf

WORKDIR /pdf

COPY dockerImage.txt dockerImage.txt
RUN pip3 install -r dockerImage.txt 

RUN apt update && apt install -y ocrmypdf

COPY . .

CMD python3 pdf.py
