# Nexus Placement Portal

A comprehensive and modern Placement Portal designed to connect college students with top-tier companies. This platform is built with an industry-standard Flask Application Factory architecture, utilizing Flask Blueprints for scalable route management.

## Features

* **Three-Tier User Roles**:
  * **Students**: Build professional profiles (CGPA, skills, resume), view active placement drives, and apply for jobs.
  * **Companies**: Register HR accounts, post customizable placement drives (Full-time/Internships, CTC, eligibility criteria), and manage application statuses (Shortlist, Interview, Select, Reject).
  * **Admin (College TPO)**: Oversee the platform through a powerful dashboard. Approve company registrations, verify drives, and manage/blacklist users.
* **Premium UI/UX**: Custom-designed using Vanilla CSS for a beautiful, responsive, and glassmorphism-inspired aesthetic. No heavy CSS frameworks attached.
* **PostgreSQL Ready**: Fully configured to connect to PostgreSQL via environment variables while relying on SQLite for rapid local development out of the box.

## Project Structure

```text
PLACEMENT_PORTAL/
├── app/
│   ├── __init__.py           # Application Factory Setup
│   ├── extensions.py         # SQLAlchemy & LoginManager instances
│   ├── models.py             # Database Schema (User, Drive, App)
│   ├── routes/
│   │   ├── admin.py          # Admin Dashboard & Approvals
│   │   ├── auth.py           # Login, Logout, Registrations
│   │   ├── company.py        # Company Dashboard & Drive Postings
│   │   ├── main.py           # Landing Page
│   │   ├── student.py        # Student Dashboard & Applications
│   ├── static/
│   │   └── css/style.css     # Global Premium Vanilla CSS
│   ├── templates/            # Jinja2 Layouts & HTML pages
├── .env                      # Environment Variables (DB Credentials)
├── config.py                 # Configuration loader
├── requirements.txt          # Python dependencies
└── run.py                    # Flask Startup Script
```

## Setup & Installation

Follow these steps to get the portal running on your local machine.

### 1. Create a Virtual Environment (Optional but Recommended)
```powershell
python -m venv myenv
myenv\Scripts\activate
```

### 2. Install Dependencies
Install all required libraries including Flask, SQLAlchemy, and Postgres binary:
```powershell
pip install -r requirements.txt
```

### 3. Configure the Database (`.env`)
By default, the application runs on SQLite (`placement.db`). 

To switch to **PostgreSQL**, open the `.env` file in the root directory and update it:
```env
SECRET_KEY=your_super_secret_key
DATABASE_URL=postgresql://username:password@localhost:5432/placement_db
```
*(Replace `username`, `password`, and `placement_db` with your actual PostgreSQL credentials.)*

### 4. Initialize the Database
Run the custom CLI command to create all tables and generate the default Admin account:
```powershell
python run.py init-db
```
The default admin account will be created:
* **Email**: `admin@portal.com`
* **Password**: `admin123`

### 5. Run the Application
Start the Flask development server:
```powershell
python run.py
```
Visit `http://127.0.0.1:5000` in your web browser.

---
*Built for modern placement cells to simplify the recruitment lifecycle.*
