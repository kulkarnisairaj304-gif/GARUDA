# 🦅 GARUDA

### Security Monitoring, Web Application Scanning & Phishing Detection Platform

GARUDA is a modular cybersecurity platform designed to help users assess web application security and detect phishing emails through a combination of rule-based security analysis and machine-learning-based detection.

The current implementation provides a FastAPI-based backend with authentication, project and application management, security scanning, phishing analysis, PostgreSQL persistence, JWT authentication, and an ML-powered phishing detection engine.

> **Project Status:** Active Development
> **Backend:** FastAPI + Python
> **Database:** PostgreSQL
> **ML:** TF-IDF + Logistic Regression

---

## 📌 Overview

Modern applications face multiple security threats, including insecure web configurations, missing security headers, phishing emails, and other attack vectors.

GARUDA provides a centralized backend platform where users can:

* Create and manage security projects
* Register applications for assessment
* Perform basic web security scans
* Check HTTPS configuration
* Detect missing security headers
* Analyze suspicious phishing emails
* Combine rule-based indicators with ML predictions
* Calculate a unified phishing risk score
* Store scan and analysis results in PostgreSQL
* Secure APIs using JWT-based authentication

The architecture is designed to be extensible so that additional security monitoring and detection capabilities can be integrated in future versions.

---

# 🎯 Objectives

The main objectives of GARUDA are:

1. Provide a centralized security assessment platform.
2. Perform automated security checks on registered web applications.
3. Identify common web security configuration issues.
4. Detect phishing emails using both rule-based and ML-based techniques.
5. Generate understandable risk scores and explanations.
6. Maintain persistent records of security scans and phishing analyses.
7. Provide secure authenticated access to platform resources.
8. Establish an architecture that can be extended into a broader security monitoring/XDR platform.

---

# 🏗️ System Architecture

```text
                         ┌──────────────────────┐
                         │       GARUDA         │
                         │  Security Platform   │
                         └──────────┬───────────┘
                                    │
                         ┌──────────▼───────────┐
                         │      FastAPI API     │
                         └──────────┬───────────┘
                                    │
          ┌─────────────────────────┼─────────────────────────┐
          │                         │                         │
          ▼                         ▼                         ▼
 ┌────────────────┐       ┌────────────────┐       ┌─────────────────┐
 │ Authentication │       │ Project / App  │       │ Security Scans  │
 │     + JWT      │       │   Management   │       │                 │
 └────────────────┘       └────────────────┘       └────────┬────────┘
                                                            │
                                                            ▼
                                                   ┌─────────────────┐
                                                   │ Scanner Engine  │
                                                   └────────┬────────┘
                                                            │
                              ┌─────────────────────────────┼────────────────────┐
                              │                             │                    │
                              ▼                             ▼                    ▼
                         HTTPS Check                Security Headers      Server Info
```

### Phishing Detection Architecture

```text
                    ┌─────────────────────┐
                    │   Phishing Email    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Phishing Engine    │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
        ┌─────────────────┐        ┌────────────────────┐
        │ Rule-Based      │        │ Machine Learning   │
        │ Detection       │        │ Detection          │
        └────────┬────────┘        └─────────┬──────────┘
                 │                           │
                 │       Rule Score           │
                 │                           │
                 └─────────────┬─────────────┘
                               ▼
                    ┌─────────────────────┐
                    │ Risk Score Engine   │
                    └──────────┬──────────┘
                               │
             ┌─────────────────┼─────────────────┐
             ▼                 ▼                 ▼
           Safe            Suspicious          Phishing
```

---

# 🚀 Key Features

## 🔐 Authentication & Authorization

GARUDA uses JWT-based authentication for protected API access.

Implemented functionality includes:

* User registration
* Secure password hashing
* User login
* JWT access token generation
* JWT token validation
* Current-user endpoint
* Protected project, application, scan, and phishing APIs

### Authentication Flow

```text
Register
   ↓
Password Hashing
   ↓
PostgreSQL
   ↓
Login
   ↓
Password Verification
   ↓
JWT Access Token
   ↓
Protected API Requests
```

---

# 📁 Project Management

Users can create and manage security projects.

Supported operations:

* Create project
* View projects
* View individual project
* Update project
* Delete project

Projects are associated with authenticated users, allowing ownership-based access control.

---

# 🌐 Application Management

Applications can be registered under projects for security assessment.

Application information can include:

* Application name
* Description
* Application type
* Base URL
* Technology
* Framework
* Environment

This information is used by the scanning subsystem when performing security checks.

---

# 🔎 Web Security Scanner

GARUDA includes a basic web security scanner implemented through the `ScannerEngine`.

The scanner performs several checks against a target application.

### HTTP Response

Verifies whether the target application responds successfully and records the returned HTTP status code.

### HTTPS Detection

Checks whether the final application URL uses HTTPS.

### Security Header Analysis

The scanner currently checks for:

* `Content-Security-Policy`
* `X-Frame-Options`
* `X-Content-Type-Options`
* `Strict-Transport-Security`

Missing headers are reported as warnings.

### Server Information

GARUDA also checks the `Server` response header and records whether server information is disclosed.

### Example Result

```json
{
  "target": "https://example.com",
  "checks": [
    {
      "check": "HTTP Response",
      "status": "Passed",
      "details": "Application responded with status code 200"
    },
    {
      "check": "HTTPS",
      "status": "Passed",
      "details": "Application is using HTTPS."
    }
  ]
}
```

---

# 🎣 Phishing Detection

GARUDA includes a hybrid phishing detection engine that combines:

### Rule-Based Detection

The system analyzes email characteristics such as:

* Urgency-based language
* Credential requests
* Account verification requests
* Suspicious URL patterns
* HTTP URLs
* IP-address-based URLs
* Suspicious keywords in URL domains
* Security-related sender keywords

### Machine Learning Detection

The ML subsystem uses:

* TF-IDF vectorization
* Logistic Regression
* Binary phishing classification
* Probability-based prediction

The trained model and vectorizer are stored inside the project and loaded during inference.

---

# 🤖 ML Pipeline

```text
Phishing Email
      │
      ▼
Text Extraction
      │
      ▼
TF-IDF Vectorization
      │
      ▼
Logistic Regression
      │
      ▼
Phishing Probability
      │
      ▼
Hybrid Risk Engine
```

The training pipeline uses an 80/20 train-test split and generates:

* Accuracy
* Classification report
* Confusion matrix

The model is trained using the phishing email dataset configured in:

```text
ml/dataset/phishing_email.csv
```

---

# 📊 Hybrid Risk Scoring

GARUDA combines rule-based analysis with ML prediction.

The current scoring strategy gives:

```text
40% → Rule-Based Score
60% → ML Score
```

The resulting score is converted into a final classification:

```text
0 – 39    → Safe
40 – 69   → Suspicious
70 – 100  → Phishing
```

The response also provides reasons explaining why an email was considered suspicious.

### Example

```json
{
  "classification": "Phishing",
  "risk_score": 87,
  "confidence": 0.87,
  "ai_probability": 0.91,
  "rule_score": 81,
  "reasons": [
    "Urgency or pressure-based language detected.",
    "Possible credential or account verification request detected."
  ]
}
```

---

# 🗄️ Database

GARUDA uses PostgreSQL with SQLAlchemy for persistent data storage.

### Current Core Models

```text
User
Project
Application
Scan
PhishingAnalysis
```

The project also includes Alembic migration infrastructure for database schema management.

### Data Flow

```text
FastAPI
   ↓
Service Layer
   ↓
Repository Layer
   ↓
SQLAlchemy
   ↓
PostgreSQL
```

---

# 🧩 Project Structure

```text
GARUDA/
│
├── app/
│   ├── ai/
│   │   ├── phishing_model.pkl
│   │   ├── tfidf_vectorizer.pkl
│   │   └── phishing_predictor.py
│   │
│   ├── api/
│   │   ├── auth_router.py
│   │   ├── project_router.py
│   │   ├── application_router.py
│   │   ├── scan_router.py
│   │   └── phishing_router.py
│   │
│   ├── auth/
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── dependencies.py
│   │   └── logger.py
│   │
│   ├── firewall/
│   │
│   ├── middleware/
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── project.py
│   │   ├── application.py
│   │   ├── scan.py
│   │   └── phishing_analysis.py
│   │
│   ├── packet/
│   ├── phising/
│   ├── reports/
│   │
│   ├── repositories/
│   │   ├── user_repository.py
│   │   ├── project_repository.py
│   │   ├── application_repository.py
│   │   ├── scan_repository.py
│   │   └── phishing_repository.py
│   │
│   ├── schemas/
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── project_service.py
│   │   ├── application_service.py
│   │   ├── scan_service.py
│   │   ├── scanner_engine.py
│   │   ├── phishing_service.py
│   │   └── phishing_engine.py
│   │
│   ├── utils/
│   │   ├── jwt_handler.py
│   │   └── security.py
│   │
│   └── main.py
│
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── ml/
│   └── train_phishing_model.py
│
├── alembic.ini
├── requirements.txt
└── README.md
```

---

# 🛠️ Technology Stack

| Category            | Technology          |
| ------------------- | ------------------- |
| Backend             | Python              |
| API Framework       | FastAPI             |
| ASGI Server         | Uvicorn             |
| Database            | PostgreSQL          |
| ORM                 | SQLAlchemy          |
| Migrations          | Alembic             |
| Authentication      | JWT                 |
| Password Security   | bcrypt              |
| Configuration       | Pydantic Settings   |
| Logging             | Loguru              |
| HTTP Requests       | Requests / HTTPX    |
| Machine Learning    | Scikit-learn        |
| NLP                 | TF-IDF              |
| ML Algorithm        | Logistic Regression |
| Model Serialization | Joblib              |

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/kulkarnisairaj304-gif/GARUDA.git
cd GARUDA
```

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

The ML training/inference components also require the packages used by the training and prediction scripts, including:

```bash
pip install pandas scikit-learn joblib requests
```

## 4. Configure Environment Variables

Create a `.env` file in the project root.

Example:

```env
APP_NAME=GARUDA
APP_VERSION=1.0.0
DEBUG=True

HOST=127.0.0.1
PORT=8000

SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

DATABASE_URL=postgresql://username:password@localhost:5432/garuda
```

Use a strong secret key for actual deployments.

## 5. Start PostgreSQL

Create a PostgreSQL database named:

```text
garuda
```

Then update `DATABASE_URL` in `.env`.

## 6. Run Database Migrations

```bash
alembic upgrade head
```

## 7. Start the Backend

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 🔗 Main API Endpoints

## Authentication

```text
POST /auth/register
POST /auth/login
GET  /auth/me
```

## Projects

```text
POST   /projects
GET    /projects
GET    /projects/{project_id}
PUT    /projects/{project_id}
DELETE /projects/{project_id}
```

## Applications

```text
POST   /applications
GET    /applications
GET    /applications/{application_id}
PUT    /applications/{application_id}
DELETE /applications/{application_id}
```

## Security Scans

```text
POST /scans/applications/{application_id}
GET  /scans
GET  /scans/{scan_id}
```

## Phishing Detection

```text
POST /phishing/analyze
```

---

# 🧪 Example Phishing Request

```json
{
  "sender": "security@example-login.com",
  "subject": "Urgent: Verify your account",
  "body": "Your account will be suspended. Please login immediately and verify your password.",
  "urls": [
    "http://192.168.1.10/login"
  ]
}
```

GARUDA analyzes the message using both rule-based indicators and the trained ML model before producing the final risk classification.

---

# 📈 Current Implementation Status

| Module                         | Status                  |
| ------------------------------ | ----------------------- |
| FastAPI backend                | ✅ Implemented           |
| JWT authentication             | ✅ Implemented           |
| Password hashing               | ✅ Implemented           |
| User management                | ✅ Implemented           |
| Project management             | ✅ Implemented           |
| Application management         | ✅ Implemented           |
| PostgreSQL integration         | ✅ Implemented           |
| SQLAlchemy ORM                 | ✅ Implemented           |
| Alembic setup                  | ✅ Implemented           |
| Security scanning              | ✅ Implemented           |
| HTTPS analysis                 | ✅ Implemented           |
| Security header analysis       | ✅ Implemented           |
| Phishing rule engine           | ✅ Implemented           |
| Phishing ML inference          | ✅ Implemented           |
| Hybrid phishing scoring        | ✅ Implemented           |
| Scan history                   | ✅ Implemented           |
| Firewall subsystem             | 🚧 Planned / Extensible |
| Packet monitoring              | 🚧 Planned / Extensible |
| Incident management            | 🚧 Planned / Extensible |
| Threat logging                 | 🚧 Planned / Extensible |
| Report generation              | 🚧 Planned / Extensible |
| Real-time WebSocket monitoring | 🚧 Planned / Extensible |
| Full XDR functionality         | 🚧 Future Development   |
| Frontend dashboard             | 🚧 Future Development   |

---

# 🔮 Future Scope

GARUDA is designed to evolve from a basic security assessment platform into a more comprehensive security monitoring platform.

Potential future improvements include:

### 🛡️ Advanced Web Security Testing

* SQL Injection detection
* Cross-Site Scripting detection
* Command Injection detection
* Path Traversal detection
* Broken Access Control analysis
* Security Misconfiguration detection
* More comprehensive vulnerability discovery

### 🌐 Network Security

* Packet capture and analysis
* Network anomaly detection
* IP reputation analysis
* Suspicious traffic detection
* Port and service monitoring

### 🚨 Incident Management

* Centralized threat logs
* Incident creation
* Severity levels
* Incident investigation workflows
* Security event correlation

### 📊 Security Dashboard

* Real-time monitoring
* Security scorecards
* Threat statistics
* Scan history visualization
* Phishing trends
* Risk distribution charts

### 🤖 Advanced AI

* Improved phishing detection models
* URL reputation analysis
* Behavioral anomaly detection
* Threat classification
* Automated security recommendations

### ⚡ Real-Time Monitoring

* WebSocket-based event streaming
* Live security alerts
* Continuous application monitoring
* Event-driven threat detection

---

# 🔒 Security Considerations

GARUDA is currently an academic/development project and should not be considered a production-grade security product without additional testing and hardening.

Before production deployment, important improvements would include:

* Secure secret management
* Removal of debug logging
* HTTPS enforcement
* Stronger authorization checks
* Input validation hardening
* Rate limiting
* Background task processing for scans
* Security testing and penetration testing
* Dependency vulnerability scanning
* Secure production database configuration

---

# 👨‍💻 Contributors

* **Sairaj Kulkarni**
* **Ejaz Sayyed** (`@Ejazsayyed12`)

---

# 📚 Academic Project

GARUDA is developed as a cybersecurity-focused academic project to explore:

* Web application security
* Security automation
* Phishing detection
* Machine learning for cybersecurity
* REST API development
* Database-backed security platforms
* Authentication and authorization
* Extensible XDR architecture

---

# ⭐ Support the Project

If you find GARUDA useful for learning or experimentation, consider giving the repository a ⭐ on GitHub.

---

# 📜 License

This project is intended for educational and research purposes.

Add an appropriate open-source license before distributing GARUDA publicly for reuse.
