FROM python:3.9.6

# Set the working directory inside the container
WORKDIR /code

# Copy requirements.txt file to the container
COPY /requirements.txt /code/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the FastAPI application code to the container
COPY ./app/ /code/app

# Expose port 80 to the outside world
EXPOSE 80

# Run the FastAPI app using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
