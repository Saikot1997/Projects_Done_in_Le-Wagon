# Use a smarter image
FROM python:3.8.12-buster

WORKDIR /prod

# First, pip install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Then only, install taxifare!
COPY taxifare taxifare
COPY setup.py setup.py
RUN pip install .

# Recreate local storage structure
COPY Makefile Makefile
RUN make reset_local_files

# Use a lighter image optimized for TensorFlow
FROM tensorflow/tensorflow:2.10.0

# Copy the installed taxifare package from the previous image
COPY --from=0 /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages

# Set the working directory
WORKDIR /prod

# Set the command to run the API
CMD ["uvicorn", "taxifare.api.fast:app", "--host", "0.0.0.0", "--port", "$PORT"]

# Expose the port
EXPOSE 8000
