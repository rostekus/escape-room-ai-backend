FROM python:3.8-slim


RUN apt-get update && \
    apt-get install -y --no-install-recommends

RUN apt-get install ffmpeg -y
RUN python3.8 -m pip install --upgrade pip==22.0.4
RUN python3.8 -m pip install --upgrade setuptools wheel

COPY requirements.txt /opt/program/requirements.txt
RUN python3.8 -m pip install -r /opt/program/requirements.txt


ENV PATH="/opt/program:${PATH}"
# ENV GOOGLE_APPLICATION_CREDENTIALS="/opt/program/cred.json"
RUN mkdir -p /opt/program
COPY . /opt/program
WORKDIR /opt/program
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]