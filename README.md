# Library Management System

A Django-based web application for managing library operations, including book management, role-based access control, and borrowing/returning workflows.

This project is designed with a clean architecture, reusable mixins, and permission-based access control, making it suitable for learning purposes as well as academic and portfolio use.

---

## Features

### User Roles

- Admin
- Librarian
- Member
Each role has specific permissions defined using Django’s permission and group system.

### Book Management
Book Management

- List and search books
- View book details
- dd new books (permission required)
- Edit book information (permission required)
- Delete books (permission required)

### Borrowing System

- Borrow available books (permission required)
- Return borrowed books
- Track active borrow records
- Edit borrow status based on user role
- Prevent borrowing unavailable books

### Technical Highlights

- Class-Based Views (CBVs)
- Custom mixins for:
  - Queryset reuse
  - Permission handling
  - Borrow status annotations
- Atomic transactions for borrow/return logic
- Clean and reusable templates (DRY principle)
- Bootstrap-based UI

---

## Prerequisites

- Python 3.11+
- Django 5.2+
- Other dependencies listed in requirements.txt

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Setup & Usage

1. Create local settings
Create a file named local_settings.py inside the confg directory and define:

```bash
SECRET_KEY = 'your-secret-key'
DEBUG = True
```

2. Apply migrations

```bash
python manage.py migrate
```

3. Create user roles and permissions

```bash
python manage.py setup_roles
```

4. Create a superuser

```bash
python manage.py createsuperuser
```

5. Run the development server

```bash
python manage.py runserver
```

---

## Notes

- This project is built entirely with Django and follows Django best practices.
- It focuses on:
  - Clean separation of concerns
  - Role-based access control
  - Readable and maintainable code
- Suitable for:
  - Learning Django CBVs and permissions
  - Academic projects
  - Portfolio and job applications

---

## Future Improvements (Optional)

- Due date for borrowed books
- Support multiple copies per book
- Borrow history per user
- API version (Django REST Framework)
- Unit and integration tests