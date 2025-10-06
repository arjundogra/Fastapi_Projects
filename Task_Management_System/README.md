# Task Management System
Task Management System with JWT Authentication (Access + Refresh Tokens) and role-based task assignment.

## Features:
1. User Management
2. Task Management
3. Role Based Access
4. Access + Refresh Token 

## Folder Structure
task_manager/
│── main.py
│── database_connection.py
│── models/
│    └── users.py
│    └── tasks.py
│── schemas/
│    └── users.py
│    └── tasks.py
│── routes/
│    └── users.py
│    └── tasks.py
│── core/
│    └── security.py   # JWT, refresh token logic
│── .env



## Checklist:
User Authentication
JWT Token on Login
Refresh token send via Cookies
Route for Refresh Token

## Schemas
Users: 
    Create -> id, email, name, role, password, created_on
    Login -> email, password  (Return JWT + Refresh Token)
    Refresh Token -> endpoint

Tasks:
    Create -> id, task_name, description, status, due_date , created_on, updated_on, assigned_to, created_by

