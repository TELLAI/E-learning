FROM python:latest

WORKDIR /app


ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

COPY . .
# Copy the current directory . 
# in the project to the workdir . in the image.

RUN pip3 install flask mysql-connector-python bs4 requests python-dotenv

# COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

EXPOSE 4020
# container is listening on port 4020



CMD ["python", "app.py"]
# set the default command for the container to flask run


# https://betterprogramming.pub/the-essential-docker-dockerfile-and-docker-compose-cheat-sheet-8bf1c42876c1
