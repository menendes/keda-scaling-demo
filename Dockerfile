# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Install Poetry
RUN pip install poetry

# Set the working directory in the container
WORKDIR /app

# Copy the pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock /app/

# Install the dependencies using Poetry
RUN poetry install --no-root

# Copy the rest of the project files
COPY . /app

# Set the default command to run the consumer or producer script
# You can override this command when running the container
CMD ["poetry", "run", "python", "consumer/consumer.py"]
