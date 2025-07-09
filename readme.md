# 📝 FastAPI To-Do List Application (with JWT Authentication)

This is a backend API for a **Personal To-Do List** application built using **FastAPI** and **PostgreSQL**. The API supports full **CRUD** operations and implements secure **JWT-based authentication** to ensure users can only access and manage their own to-do items.

---

## 🚀 Features

- User registration & JWT login
- Create, read, update, and delete personal to-do items
- Role-based access: users can only manage their own todos
- Email and full name validation
- Automatic timestamp management (`created_at`, `updated_at`)
- Clean RESTful API with proper status codes and responses

---

## 🧱 Tech Stack

- **FastAPI** (Web framework)
- **PostgreSQL** (Database)
- **SQLAlchemy** (ORM)
- **Pydantic** (Data validation and serialization)
- **JWT** (Authentication)

---

## 🗃️ Data Model

### ✅ User
- `id`: Integer (Primary Key)
- `full_name`: String (required)
- `email`: String (valid email)
- `password`: String (hashed)

### ✅ To-Do
- `id`: Integer (Primary Key)
- `user_id`: Foreign key (links to User)
- `task`: String (description of task)
- `completed`: Boolean (default: `False`)
- `created_at`: Timestamp (auto)
- `updated_at`: Timestamp (auto)

---

## 🔐 Authentication

- JWT-based authentication using access tokens
- Only authenticated users can access the `/todos` endpoints
- Each user can only manage their own to-do items

---

## 📬 API Endpoints

| Method | Endpoint         | Description                         |
|--------|------------------|-------------------------------------|
| GET    | `/todos`         | Get list of authenticated user's todos (paginated) |
| POST   | `/todos`         | Create a new to-do item             |
| PUT    | `/todos/{id}`    | Update an existing to-do (partial OK) |
| DELETE | `/todos/{id}`    | Delete a specific to-do item        |

---

## 🧪 Example JSON Payloads

### ➕ Create To-Do
```json
{
  "task": "Buy groceries"
}
```

### ✅ Update To-Do
```json
{
  "task": "Buy groceries and cook dinner",
  "completed": true
}
```

---

## ⚙️ Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/regmiaashish/todo-fastapi.git
cd todo-fastapi
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure `.env` file
Create a `.env` file and set the following variables:
```
DATABASE_URL=postgresql://user:your_password@localhost:5432/your_database
SECRET_KEY=your_jwt_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 5. Run migrations and start server
```bash
uvicorn main:app --reload
```

---

## 🔐 Authentication Usage (with Postman)

1. **Register a new user**
   - `POST /register`

2. **Login to receive access token**
   - `POST /token`

3. **Authorize in Postman**
   - Set token in `Authorization` header as `Bearer <your_token>`

---

## 📁 Folder Structure
```
.
├── main.py
├── models.py
├── schemas.py
├── auth.py
├── database.py
├── .env
└── README.md
```

---

## ✍️ Author

**Aashish Regmi**  
Python/Django & FastAPI Developer  
[GitHub Profile](https://github.com/regmiaashish)

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).