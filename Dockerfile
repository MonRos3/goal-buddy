# syntax=docker/dockerfile:1

FROM python:3.11.8-bookworm

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

ADD src /src
WORKDIR /src

COPY src /src

# Environment Variables
ENV FLASK_APP=/src/app/__init__.py
ENV SECRET_KEY='super-duper-secret-key123'
ENV SQLALCHEMY_DATABASE_URI='127.0.0.1'

# Change to port 5001 to work with macOS
# AirPlay uses port 5000 on macOS 
EXPOSE 5001
CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]

# Instructions for Dockerfile
# Run these commands:
# docker build -t app .
# docker run -p 5001:5001 app