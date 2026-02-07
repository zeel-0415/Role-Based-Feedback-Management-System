# Role-Based Feedback Management System

## 📌 Overview

This project is a backend-driven **Role-Based Feedback Management System** that allows users to securely submit, manage, and update their feedback while providing administrators with moderation capabilities through a dedicated dashboard.

The application is designed using production-oriented principles such as modular architecture, authentication, access control, and secure data handling.

---

## 🚀 Features

### 👤 User Features

* User Registration & Login
* Secure password hashing
* Submit feedback
* Update previously submitted feedback
* View personal feedback history
* Logout functionality

### 🛠️ Admin Features

* Dedicated admin dashboard
* View all user feedback
* Edit feedback
* Soft delete feedback (prevents permanent data loss)
* Role-based access control

---

## 🧠 Architecture Highlights

* **Modular Design using Flask Blueprints** for separation of concerns
* **SQLAlchemy ORM** for structured database interaction
* **Session-based Authentication** using Flask-Login
* **Ownership Validation** to ensure users can only modify their own data
* **Soft Delete Strategy** for auditability and data protection

---

## 🧰 Tech Stack

**Backend:**

* Python
* Flask
* SQLAlchemy (ORM)
* Flask-Login
* Werkzeug (Password Hashing)

**Database:**

* SQLite (Development)

  * Can be easily migrated to PostgreSQL for production.

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone <your-repo-url>
cd feedback-system
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate it:

**Windows:**

```bash
venv\Scripts\activate
```

**Mac/Linux:**

```bash
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install flask flask_sqlalchemy flask_login werkzeug
```

---

### 4️⃣ Run the Application

```bash
python app.py
```

Server will start at:

```
http://127.0.0.1:5000
```

---

## 🔐 Default Admin Credentials

```
Username: admin
Password: admin123
```

*(Created automatically when the app runs for the first time)*

---

## 📊 Database

The application uses SQLite for simplicity during development.

To reset the database:

1. Stop the server
2. Delete the `instance` folder or `.db` file
3. Restart the application

---

## 🔒 Security Practices Implemented

* Password hashing (no plain-text storage)
* Protected routes with authentication
* Role-based authorization
* Ownership checks
* Soft deletes for safer data management

---

## 📈 Future Improvements

* Pagination for admin dashboard
* Search & filtering
* REST API support
* JWT authentication for distributed systems
* Docker containerization
* CI/CD pipeline integration

---

## 🎯 Project Goal

The goal of this project was to simulate a real-world moderation workflow while focusing on backend design principles such as scalability, maintainability, and secure access patterns.

---

## 👨‍💻 Author

**Akil Pathan**
Backend & Full Stack Developer

---

⭐ If you found this project useful, consider giving it a star!
