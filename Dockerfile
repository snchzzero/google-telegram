FROM python:3.10.4

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/google_sheets_cbr

COPY ./requirements.txt /usr/srs/requirements.txt
RUN pip install -r /usr/srs/requirements.txt

COPY . /usr/src/google_sheets_cbr

# EXPOSE 8000
CMD ["python", "main.py"]