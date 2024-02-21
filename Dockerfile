# Use the official Python image
# FROM python:3.9-slim
#FROM digi0ps/python-opencv-dlib

FROM python:3.9-slim

RUN apt-get -y update
# for dlib
RUN apt-get install -y build-essential cmake
# for opencv
# RUN apt-get install -y libopencv-dev

# pip instlal
RUN pip install dlib==19.17.0
#  && pip install opencv-python==4.1.0.25

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose the port that FastAPI is running on
EXPOSE 8001

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]