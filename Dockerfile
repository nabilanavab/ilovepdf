FROM python:3.11
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

RUN apt-get install -y tree
RUN tree

CMD python3 __main__.py
