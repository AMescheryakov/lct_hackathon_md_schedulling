# Doctor Schedul
## Project structure
```
├── css
│   ├── menu.css.json            # JSON file containing menu CSS styles
│   └── style.css                # CSS file for general styling
├── Dockerfile                   # Docker configuration file for containerization
├── doctor_ui                    # Main application directory
│   ├── app.py                   # Main application script
│   ├── __init__.py              # Package initialization file
│   ├── settings.py              # Application settings/configuration
│   ├── state                    # Directory for managing application state
│   │   ├── __init__.py          # State package initialization file
│   │   └── state.py             # Module for defining application state
│   ├── style.py                 # Module for managing application styles
│   ├── user.py                  # Module for handling user-related functionalities
│   └── views                    # Directory for Flask views
│       ├── access.py           # View for managing user access
│       ├── calendar.py         # View for calendar functionality
│       ├── __init__.py         # Views package initialization file
│       ├── login.py            # View for user login
│       ├── logout.py           # View for user logout
│       ├── registry.py         # View for managing doctor registry
│       ├── speciality.py       # View for managing doctor specializations
│       └── vacations.py        # View for managing doctor vacations
├── pyproject.toml               # Project metadata and dependencies (e.g., using Poetry)
├── README.md                    # Project documentation
└── setup.py                     # Setup script for packaging and distribution

```
## Run UI

To run the app use Docker:  

`docker build -t doctor_app src/frontend`  
Run container:  
`docker run -v /path/to/data/test_data:/app/data -p 8501:8501 doctor_app`
