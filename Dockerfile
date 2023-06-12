FROM python:latest
RUN mkdir /pdf && chmod 777 /pdf

WORKDIR /pdf

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY libgenesis/requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN apt update
RUN apt install -y ocrmypdf
RUN apt install -y wkhtmltopdf

COPY . .

CMD python3 pdf.py
