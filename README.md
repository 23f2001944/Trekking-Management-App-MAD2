# 🥾 Trekking Management Application (TMA)

A full-stack web application for managing trekking activities. The system supports three user roles:

- **Admin** – Creates and manages treks, staff, and users.
- **Trek Staff** – Manages assigned treks and participants.
- **Trekker (User)** – Browses, books, and tracks trekking history.

---

## 🚀 Tech Stack

### Backend
- Flask
- Flask-JWT-Extended
- SQLAlchemy
- SQLite

### Frontend
- Vue 2
- Bootstrap 

### Other Technologies
- Redis (Flask-Caching)
- Celery (Background Jobs)

---

## 📂 Project Structure

```
backend/
frontend/
README.md
requirements.txt
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/23f2001944/Trekking-Management-App-MAD2
cd Trekking-Management-App-MAD2
```

---

### 2. Backend Setup

```bash
cd backend

python -m venv venv
```

#### Activate the virtual environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Start the backend server:

```bash
python app.py
```

The backend will run at:

```
http://localhost:5000
```

On the first run:
- SQLite database is created automatically.
- Default admin account is seeded automatically.

---

### 3. Frontend Setup

```bash
cd frontend

npm install
npm run dev
```

The frontend will be available at:

```
http://localhost:5173
```

---

## 🗄️ Redis

Ensure a Redis server is running before starting the application.

Default Redis URL:

```
redis://localhost:6379
```

Redis is used for:
- API response caching
- Background task support (Celery)

---

## 👤 Default Admin Login

| Email | Password |
|-------|----------|
| admin@local.com | Admin@123 |

---

## 👥 User Roles

### Admin
- Create, update and delete treks
- Assign trek staff
- Manage users
- View dashboard statistics

### Trek Staff
- Manage assigned treks
- Update trek status
- Modify trek capacity
- View participant list

### Trekker (User)
- Register and login
- Browse available treks
- Book treks
- View booking history

---

## ✨ Features

- JWT Authentication
- Role-Based Access Control
- Trek Management
- Trek Booking System
- Dashboard Analytics
- Redis Caching
- Background Jobs using Celery
- Responsive Bootstrap UI

---

## 📌 Running the Complete Application

Start the services in separate terminals.

### Terminal 1

```bash
redis-server
```

### Terminal 2

```bash
cd backend
python app.py
```

### Terminal 3

```bash
cd backend
celery -A celery_app.celery worker --loglevel=info --pool=solo
```

### Terminal 4

```bash
cd backend
celery -A celery_app.celery beat --loglevel=info
```

### Terminal 5

```bash
cd frontend
npm run dev
```

---

## 📄 License

This project was developed as part of the **Modern Application Development II (MAD-II)** coursework.