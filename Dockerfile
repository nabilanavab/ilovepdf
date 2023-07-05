FROM python:latest
RUN mkdir /pdf && chmod 777 /pdf

WORKDIR /ILovePDF

COPY ILovePDF/requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ILovePDF/libgenesis/requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN apt update
RUN apt install -y ocrmypdf
RUN apt install -y wkhtmltopdf

COPY /ILovePDF .
COPY /ILovePDF/web .

CMD gunicorn web:app & python3 __main__.py
