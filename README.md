# Portfolio Django Project

A Django-based portfolio management system with gamification elements.

## Features

- User authentication and profile management
- Portfolio file management
- Gamification system with XP, achievements, and character classes
- University templates and requirements management
- RESTful API with JWT authentication

## Setup

1. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with the following content:
```
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
MEDIA_ROOT=media
STATIC_ROOT=static
```

4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## API Endpoints

- `/api/register/` - User registration
- `/api/login/` - User login (JWT token)
- `/api/profile/` - User profile management
- `/api/files/` - Portfolio file management

## Project Structure

- `users/` - User authentication and profile management
- `portfolio/` - Portfolio file management
- `rpg/` - Gamification system
- `universities/` - University templates and requirements

## Development

The project uses:
- Django REST Framework for API development
- JWT for authentication
- SQLite for development database
- Tailwind CSS for styling (optional) 