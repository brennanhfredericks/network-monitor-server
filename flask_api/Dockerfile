# Use python base image
FROM python:3.8

# Set the working directory to /app
WORKDIR /app

# Copy the current directory
COPY . /app

# install python package
RUN pip install -r requirements.txt

# set flask config
#ENV YOURAPPLICATION_SETTINGS=./instance/config.py

# run the command to start uWSGI
CMD ["python3","run.py"]