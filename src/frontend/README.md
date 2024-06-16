# Doctor Schedul

## Run UI

To run the app use Docker:  

`docker build -t doctor_app src/frontend`
Run container:  
`docker run -v /path/to/data/test_data:/app/data -p 8501:8501 doctor_app`
