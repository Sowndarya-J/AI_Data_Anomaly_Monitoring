# AI Data Anomaly Monitoring System

An end-to-end **AI-powered transaction anomaly monitoring system** built using Python, Machine Learning, FastAPI, MySQL, Docker, and automated testing.

The system processes e-commerce transaction data, performs data cleaning and ETL, detects potentially anomalous transactions, stores/loads database information, exposes monitoring results through REST APIs, and supports containerized deployment using Docker.

---

## 🚀 Project Overview

The goal of this project is to build a data monitoring pipeline that can identify unusual transaction records automatically.

The project covers the complete workflow:

```text
Raw Transaction Data
        ↓
Data Cleaning
        ↓
ETL Pipeline
        ↓
Anomaly Detection
        ↓
Anomaly Results
        ↓
MySQL Database
        ↓
FastAPI REST API
        ↓
Docker Container
        ↓
API Monitoring
```

The project also includes automated tests covering API behavior, data quality, ETL, database connectivity, model functionality, integration, functional behavior, and regression checks.

---

## 🎯 Objectives

* Process transaction datasets automatically.
* Clean and validate transaction data.
* Build an ETL pipeline.
* Detect anomalous transactions using an anomaly detection model.
* Generate anomaly monitoring results.
* Store transaction data in MySQL.
* Provide REST APIs for monitoring results.
* Add API health monitoring.
* Containerize the API using Docker.
* Implement automated testing using Pytest.
* Maintain the project using Git and GitHub.

---

## 🛠️ Technologies Used

| Technology             | Purpose                              |
| ---------------------- | ------------------------------------ |
| Python                 | Core programming language            |
| Pandas                 | Data processing and analysis         |
| NumPy                  | Numerical operations                 |
| Scikit-learn           | Machine learning / anomaly detection |
| FastAPI                | REST API development                 |
| Uvicorn                | API server                           |
| MySQL                  | Database                             |
| mysql-connector-python | Python-MySQL connection              |
| Pytest                 | Automated testing                    |
| Docker                 | Containerization                     |
| Git                    | Version control                      |
| GitHub                 | Source code repository               |

---

## 📁 Project Structure

```text
AI_Data_Anomaly_Monitoring/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── data/
│   ├── transactions.csv
│   │
│   ├── processed/
│   │   └── ecommerce_transactions_clean.csv
│   │
│   └── raw/
│       ├── ecommerce_transactions.csv
│       └── generate_dataset.py
│
├── reports/
│   └── anomaly_results.csv
│
├── dashboard/
│   └── app.py
│
├── src/
│   │
│   ├── anomaly_detection/
│   │   ├── __init__.py
│   │   ├── anomaly_detector.py
│   │   └── model.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── main.py
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   └── db_connection.py
│   │
│   ├── data_processing/
│   │   ├── __init__.py
│   │   ├── data_cleaning.py
│   │   └── etl_pipeline.py
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   └── logger.py
│   │
│   └── load_to_mysql.py
│
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_data.py
│   ├── test_database.py
│   ├── test_data_quality.py
│   ├── test_etl.py
│   ├── test_functional.py
│   ├── test_integration.py
│   ├── test_model.py
│   └── test_regression.py
│
├── .dockerignore
├── .gitignore
├── Dockerfile
├── main.py
├── requirements.txt
└── README.md
```

---

# 🔄 Data Processing Pipeline

## 1. Raw Data

The project starts with e-commerce transaction data stored under:

```text
data/raw/ecommerce_transactions.csv
```

The dataset contains transaction-related information that is used for anomaly monitoring.

---

## 2. Data Cleaning

The data cleaning module performs preprocessing and validation before the data is used by the anomaly detection pipeline.

Cleaned data is stored under:

```text
data/processed/ecommerce_transactions_clean.csv
```

---

## 3. ETL Pipeline

The ETL pipeline performs:

### Extract

Reads transaction data from the source dataset.

### Transform

Performs cleaning, validation, and required transformations.

### Load

Prepares the processed data for further analysis and database loading.

---

# 🤖 Anomaly Detection

The anomaly detection module is located at:

```text
src/anomaly_detection/
```

Important files:

```text
model.py
anomaly_detector.py
```

The model analyzes transaction records and identifies potentially unusual transactions.

The generated results are stored in:

```text
reports/anomaly_results.csv
```

Each transaction is classified into a status such as:

```text
NORMAL
ANOMALY
```

---

# 📊 Current Project Result

The completed pipeline produced:

```text
Total Transactions : 998
Normal Transactions: 948
Anomalies Detected  : 50
```

This means the monitoring pipeline successfully processed the transaction dataset and identified anomalous records.

---

# 🗄️ MySQL Database

The project uses MySQL for database connectivity.

Database connection logic is implemented in:

```text
src/database/db_connection.py
```

The application uses environment variables for database configuration.

Example:

```text
DB_HOST
DB_PORT
DB_USER
DB_PASSWORD
DB_NAME
```

Example configuration:

```text
DB_HOST=host.docker.internal
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=anomaly_monitoring
```

> Do not commit real database passwords or credentials to GitHub.

---

# 🌐 FastAPI REST API

The API is implemented using FastAPI.

Main API file:

```text
src/api/main.py
```

The API provides endpoints for:

* API status
* Health monitoring
* Transaction summary
* All anomalies
* Individual transaction anomaly information

---

## API Endpoints

### 1. Home

```http
GET /
```

Example:

```text
http://localhost:8000/
```

Response:

```json
{
  "message": "AI Data Anomaly Monitoring API",
  "status": "running"
}
```

---

### 2. Health Check

```http
GET /health
```

Example:

```text
http://localhost:8000/health
```

The endpoint checks:

* API status
* MySQL database connection
* Availability of anomaly results

Example successful response:

```json
{
  "status": "healthy",
  "database": "connected",
  "anomaly_results": true
}
```

---

### 3. Transaction Summary

```http
GET /summary
```

Example:

```text
http://localhost:8000/summary
```

Example response:

```json
{
  "total_transactions": 998,
  "normal_transactions": 948,
  "anomalies_detected": 50
}
```

---

### 4. Get All Anomalies

```http
GET /anomalies
```

Example:

```text
http://localhost:8000/anomalies
```

Returns the transactions identified as anomalies.

---

### 5. Get Individual Transaction

```http
GET /anomalies/{transaction_id}
```

Example:

```text
http://localhost:8000/anomalies/1
```

Replace `1` with an available transaction ID from the dataset.

---

# 🐳 Docker Deployment

The API is containerized using Docker.

Docker configuration is defined in:

```text
Dockerfile
```

The project uses:

```dockerfile
FROM python:3.10-slim
```

The Docker container installs the required Python dependencies and starts the FastAPI application using Uvicorn.

---

## Build Docker Image

From the project root:

```powershell
docker build -t ai-data-anomaly-monitoring .
```

---

## Run Docker Container

Example:

```powershell
docker run -d `
  --name ai-anomaly-api `
  -p 8000:8000 `
  --add-host=host.docker.internal:host-gateway `
  -e DB_HOST=host.docker.internal `
  -e DB_PORT=3306 `
  -e DB_USER=root `
  -e DB_PASSWORD=YOUR_PASSWORD `
  -e DB_NAME=anomaly_monitoring `
  ai-data-anomaly-monitoring
```

Check running containers:

```powershell
docker ps
```

---

# 🧪 Testing

The project contains a comprehensive Pytest test suite.

Test categories include:

```text
API Testing
Data Testing
Database Testing
Data Quality Testing
ETL Testing
Functional Testing
Integration Testing
Model Testing
Regression Testing
```

Run all tests:

```powershell
pytest -v
```

The project successfully reached:

```text
31 passed
```

Example:

```text
tests/test_regression.py::test_transaction_amounts_are_valid PASSED
```

Final result:

```text
31 passed in 1.25s
```

---

# 🔁 CI/CD

GitHub Actions is configured using:

```text
.github/workflows/ci.yml
```

The workflow helps automatically validate the project when changes are pushed to GitHub.

The CI pipeline can run automated tests and help identify issues before changes are merged.

---

# 📋 Logging

Application logging utilities are maintained under:

```text
src/utils/logger.py
```

Logging helps track application execution and troubleshooting information.

---

# 📈 Dashboard

The project also contains a dashboard component:

```text
dashboard/app.py
```

It can be used as the presentation layer for displaying anomaly monitoring information.

---

# ⚙️ Installation

## 1. Clone Repository

```bash
git clone https://github.com/Sowndarya-J/AI_Data_Anomaly_Monitoring.git
```

Move into the project:

```bash
cd AI_Data_Anomaly_Monitoring
```

---

## 2. Create Virtual Environment

Windows:

```powershell
python -m venv venv
```

Activate:

```powershell
venv\Scripts\activate
```

---

## 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

---

## 4. Run Tests

```powershell
pytest -v
```

---

## 5. Run FastAPI Locally

```powershell
uvicorn src.api.main:app --reload
```

API:

```text
http://localhost:8000
```

FastAPI documentation:

```text
http://localhost:8000/docs
```

---

# 🔐 Security

Sensitive information should not be hardcoded in the source code.

Database credentials should be provided through environment variables.

For example:

```text
DB_PASSWORD=your_password
```

Do not commit:

```text
.env
passwords
API keys
database credentials
```

The `.gitignore` file should be used to prevent sensitive or unnecessary files from being committed.

---

# 🧰 Commands Used During Development

### Check Git status

```powershell
git status
```

### Add files

```powershell
git add .
```

### Commit changes

```powershell
git commit -m "Add Docker deployment configuration"
```

### Push to GitHub

```powershell
git push origin main
```

### Check Docker version

```powershell
docker --version
```

### Check Docker information

```powershell
docker info
```

### Build image

```powershell
docker build -t ai-data-anomaly-monitoring .
```

### List running containers

```powershell
docker ps
```

### Stop container

```powershell
docker stop ai-anomaly-api
```

### Remove container

```powershell
docker rm ai-anomaly-api
```

### Check API

```powershell
Invoke-RestMethod http://localhost:8000/
```

### Check API health

```powershell
Invoke-RestMethod http://localhost:8000/health
```

### Check anomaly summary

```powershell
Invoke-RestMethod http://localhost:8000/summary
```

---

# 🧠 What I Learned From This Project

Through this project, I worked with:

* Python project structure
* Data preprocessing
* ETL pipelines
* Data quality validation
* Anomaly detection
* Machine learning workflow
* Pandas
* MySQL database connectivity
* FastAPI
* REST APIs
* API health checks
* Pytest
* Unit testing
* Integration testing
* Regression testing
* Docker
* Docker image creation
* Docker containers
* Environment variables
* Git
* GitHub
* GitHub Actions
* CI testing
* API deployment concepts

---

# 💼 Resume Description

### AI Data Anomaly Monitoring System

**Technologies:** Python, Pandas, Scikit-learn, FastAPI, MySQL, Docker, Pytest, GitHub Actions

* Developed an end-to-end transaction anomaly monitoring system using Python, data processing, and machine learning techniques.
* Implemented data cleaning and ETL pipelines to prepare e-commerce transaction data for anomaly detection.
* Built FastAPI REST endpoints for transaction summaries, anomaly records, individual transaction lookup, and application health monitoring.
* Integrated MySQL for database connectivity and configured container-to-host database communication using Docker.
* Containerized the API using Docker and implemented automated testing with Pytest across API, data, ETL, model, integration, functional, and regression components.
* Achieved **31/31 automated tests passing** and successfully deployed the API as a Docker container.

---

# 🎤 Interview Explanation

### Short Version

> "I developed an AI-based Data Anomaly Monitoring System for e-commerce transaction data. I created a data processing and ETL pipeline, performed data validation, and implemented anomaly detection to identify unusual transactions. The results are exposed through a FastAPI REST API and integrated with MySQL. I also containerized the API using Docker and created automated tests using Pytest. The final test suite had 31 tests passing successfully."

### Technical Flow

```text
Dataset
   ↓
Data Cleaning
   ↓
ETL Pipeline
   ↓
Anomaly Detection
   ↓
Anomaly Results CSV
   ↓
MySQL
   ↓
FastAPI
   ↓
Docker
   ↓
REST API
```

---

# 👩‍💻 Author

**Sowndarya J**

MCA Graduate | Aspiring Software / Data / ML Engineer

GitHub:

https://github.com/Sowndarya-J

---

## ⭐ Project Status

```text
Project Status: Completed

Data Processing       ✅
ETL Pipeline          ✅
Anomaly Detection     ✅
MySQL Integration     ✅
FastAPI                ✅
REST APIs             ✅
Automated Testing     ✅
Docker Deployment     ✅
GitHub                 ✅
CI Workflow            ✅
Documentation          ✅
```
