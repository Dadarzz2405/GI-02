# Rohis Management System

## Overview

The Rohis Management System is a web-based application for managing Rohis (Rohani Islam) activities in schools. It digitizes member management and attendance tracking, replacing manual paper-based processes. The system supports multiple user roles (admin, ketua, pembina, member) with role-based access control for different features.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: Flask (Python) - chosen for simplicity and rapid development
- **Application Entry**: `app.py` serves as the main application file with route definitions
- **Database ORM**: SQLAlchemy with Flask-SQLAlchemy extension
- **Authentication**: Flask-Login for session management, Flask-Bcrypt for password hashing
- **Database Migrations**: Flask-Migrate with Alembic for schema versioning

### Data Models (models.py)
- **User**: Core entity with role-based permissions (admin, ketua, pembina, member), profile pictures, class assignments, and PIC associations
- **Session**: Represents attendance sessions with date, name, and PIC assignment
- **Attendance**: Links users to sessions with status tracking (present, absent, late, excused)
- **Pic**: Person-in-charge groups for organizing members
- **Division**: Organizational divisions for member categorization
- **Notulensi**: Meeting notes linked to sessions

### Frontend Architecture
- **Templating**: Jinja2 templates extending a base layout (`base.html`)
- **Styling**: Custom CSS (`style.css`) with Bootstrap 5 for responsive design
- **JavaScript**: Vanilla JS for attendance marking and chat functionality
- **UI Framework**: Bootstrap 5 with Font Awesome icons and Inter font family

### AI Integration
- **Chatbot**: Groq API integration for Islamic educational assistance (`ai.py`)
- **Formatter**: LLM-powered attendance report formatting (`formatter.py`)
- **Navigation**: Chatbot can direct users to different pages via command parsing

### Key Routes Structure
- `/login` - Authentication
- `/dashboard_admin`, `/dashboard_member` - Role-specific dashboards
- `/attendance` - Attendance marking
- `/member-list` - Member directory
- `/profile` - User profile management
- `/api/attendance` - REST endpoint for attendance operations

### Role-Based Access Control
- Admins and pembina have full attendance marking permissions
- Core users (admin, ketua) have elevated privileges
- Members can mark attendance only if explicitly granted permission via `can_mark_attendance` field

## External Dependencies

### Database
- **SQLite**: File-based database stored at `database.db` in the project root
- Simple setup, no external database server required

### AI/LLM Service
- **Groq API**: Used for chatbot responses and attendance formatting
- Requires `GROQ_API_KEY` environment variable
- Models used: `llama-3.1-8b-instant`

### Python Packages (key dependencies)
- Flask ecosystem: Flask, Flask-SQLAlchemy, Flask-Login, Flask-Bcrypt, Flask-Migrate, Flask-Cors
- Document generation: python-docx for Word document exports
- Islamic calendar: ummalqura for Hijri date conversion
- HTTP client: requests for external API calls

### Frontend CDN Resources
- Bootstrap 5.3.0
- Font Awesome 6.0.0
- Bootstrap Icons 1.10.5
- FullCalendar 6.1.11 (for calendar views)
- Quill.js 1.3.6 (for rich text editing in notulensi)
- Animate.css 4.1.1

### Production Deployment
- **WSGI Server**: Gunicorn for production deployment
- Deployed on Render.com (based on attached logs)
- Static files served from `/static` directory
- Profile uploads stored in `static/uploads/profiles`