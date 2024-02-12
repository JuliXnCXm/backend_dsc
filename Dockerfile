FROM python:alpine3.19
RUN mkdir -p /opt/api
WORKDIR /opt/api
COPY . .
RUN pip install -r requirements.txt
CMD [ "uvicorn", "main:app"]