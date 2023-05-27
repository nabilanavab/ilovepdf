FROM python:latest
RUN mkdir /pdf && chmod 777 /pdf

WORKDIR /pdf

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

RUN apt update && apt install -y ocrmypdf wkhtmltopdf

COPY . .

CMD python3 pdf.py
