FROM python:3.10

# Set the working directory
WORKDIR /code

# Copy backend requirements first to cache dependencies
COPY ./backend/requirements.txt /code/requirements.txt

# Install python dependencies  
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the backend files
COPY ./backend /code/backend

# Copy the trained model
COPY ./trained_model.keras /code/trained_model.keras

# Expose port 7860 which is required by Hugging Face Spaces
EXPOSE 7860

# Run the FastAPI server
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "7860"]
