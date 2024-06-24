FROM python:slim-buster

# Copying requirements of a project
COPY pyproject.toml /app/src/
COPY setup.py /app/src/

WORKDIR /app/src

# Copying application
COPY . /app/src/
RUN pip install -e .

CMD ["streamlit", "run", "doctor_ui/app.py"]
