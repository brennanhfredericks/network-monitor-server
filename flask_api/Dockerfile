# Use python base image
FROM python3.8

# Set the working directory to /app
WORKDIR /app

# Copy the current directory
COPY . /app

# uWSGI dependency
RUN apt-get install build-essential python-dev

# install python package
RUN pip install -r requirements.txt

# set flask config
ENV YOURAPPLICATION_SETTINGS=./instance/config.py

# run the command to start uWSGI
CMD ["uwsgi","app.ini"]