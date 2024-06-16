FROM python:slim-buster

# Copying requirements of a project
COPY pyproject.toml /app/src/
COPY setup.py /app/src/

WORKDIR /app/src

# Copying actual application
COPY ./doctor_ui /app/src/doctor_ui
RUN pip install --no-cache-dir --upgrade .

# Copy styles
COPY ./css /app/src/
CMD ["streamlit", "run", "doctor_ui/app.py"]
