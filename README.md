\# 🥛 Milk Dairy Management System



A backend-based Milk Dairy Management System designed to manage farmers, daily milk collections, payments, reports, and receipts efficiently.



The project is built using \*\*Python, FastAPI, PostgreSQL and SQLAlchemy\*\* with JWT-based authentication.



---



\## 🚀 Features



\### 🔐 Authentication

\- Admin login

\- JWT authentication

\- Protected API endpoints

\- Role-based access control



\### 👨‍🌾 Farmer Management

\- Add farmer

\- View farmers

\- View farmer by ID

\- Update farmer

\- Delete farmer

\- Unique mobile number validation



\### 🥛 Milk Collection

\- Morning/evening milk collection

\- Quantity tracking

\- Fat and SNF tracking

\- Automatic amount calculation

\- Farmer-wise collection

\- Date-wise collection

\- Daily collection summary

\- Duplicate collection prevention



\### 💰 Payment Management

\- Generate farmer payment

\- Automatic total liters calculation

\- Automatic total amount calculation

\- Payment approval

\- Mark payment as paid

\- Payment method tracking

\- Farmer payment history

\- Duplicate payment prevention



\### 📊 Reports

\- Daily milk collection report

\- Farmer-wise report

\- Date-range reports

\- Total liters

\- Total amount

\- Excel payment report



\### 📄 PDF Receipts

\- Generate payment receipt

\- Farmer details

\- Milk collection details

\- Payment information

\- Downloadable PDF receipt



---



\## 🛠️ Tech Stack



\### Backend

\- Python

\- FastAPI

\- SQLAlchemy

\- PostgreSQL

\- Pydantic



\### Authentication

\- JWT

\- OAuth2 Password Flow

\- Passlib

\- bcrypt



\### Database

\- PostgreSQL

\- SQLAlchemy ORM

\- Alembic



\### Reporting

\- ReportLab

\- OpenPyXL



\### Development Tools

\- Git

\- GitHub

\- VS Code

\- Uvicorn



---



\## 📁 Project Structure



```text

backend/

│

├── app/

│   ├── database/

│   ├── dependencies/

│   ├── models/

│   ├── routers/

│   ├── schemas/

│   ├── services/

│   ├── utils/

│   └── main.py

│

├── .gitignore

├── requirements.txt

└── README.md


## Payment Module

Payment management for farmers is under development.
