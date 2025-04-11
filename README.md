# TranSync
Arabic-to-English XLSX Translator <br/>
A tool for batch-translating `.xlsx` spreadsheets from **Arabic to English** using a locally hosted LLM in **LM Studio**.

---

## Getting Started

### Start the Application

Run the following command to build and start the containers:  

```docker-compose up```

This will: 

1. Build the Docker images for the FastAPI and Streamlit services.  
2. Start the containers and serve the application.  

---

## Features

- **Multi-sheet Excel Support**:  
  Handles Excel files with multiple sheets seamlessly.

- **Smart Cell Translation**:  
  Translates cell-by-cell **only** if Arabic text is detected.

- **Sheet Name Translation**:  
  Automatically translates and renames sheet titles.

- **Streamlit Frontend**:  
  Provides a user-friendly interface for uploading and downloading translated Excel files.  
  Hosted on <http://localhost:8080>

- **FastAPI Backend**:  
  Handles the processing and translation logic.  
  Hosted on <http://localhost:8000>  
  Interactive API documentation available at <http://localhost:8000/docs>

- **Live Reloading**:  
  Hot reloading is enabled for both FastAPI and Streamlit during development for rapid iteration.

---

## Prerequisites

Before you start, ensure the following tools are installed on your system:

- Docker  
- Docker Compose  

---

## Access the Application

- **FastAPI Backend**:  
  Visit <http://localhost:8000> to access the API.  
  Documentation is available at <http://localhost:8000/docs>  

- **Streamlit Frontend**:  
  Visit <http://localhost:8080> to interact with the frontend.  

---

## Development Workflow

### Live Reloading

Both FastAPI and Streamlit support hot reloading out of the box. Any changes you 
make to the code will automatically reflect in the running containers.  

### Stopping the Application

To stop the application, press `Ctrl+C` or run the following command:  

docker-compose down  

This will stop and remove the containers, but the built images will remain.  

---

## Directory Structure

The project structure is as follows:  

```shell
.  
├── backend/               # FastAPI application  
│   ├── main.py            # FastAPI entrypoint
│   ├── translate.py       # Translation logic for text, DataFrames, and Excel sheets using LLM
│   ├── requirements.txt   # Python dependencies for FastAPI  
│   └── Dockerfile         # Dockerfile for FastAPI
├── frontend/              # Streamlit application  
│   ├── app.py             # Streamlit entrypoint  
│   ├── Dockerfile         # Dockerfile for Streamlit
│   └── requirements.txt   # Python dependencies for streamlit 
├── data/output            # Directory to store translated Excel files
│   └── .gitkeep           # Placeholder to keep the folder tracked by Git
├── docker-compose.yml     # Docker Compose configuration  
└── README.md              # Project documentation  
```

---

## Troubleshooting

- Ensure Docker and Docker Compose are installed and running on your system.  
- Verify that the required ports (8000 and 8080) are not in use by other 
applications.  

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

