# alumni-network-management-system
A Full-Stack Alumni Networking &amp; Profile Management System built using Flask and MySQL.
# Alumni Network and Profile Management System

A full-stack web-based platform built using Flask and MySQL, designed to manage alumni data, events, and user profiles efficiently. This system allows alumni to register, log in, manage their personal and professional information, participate in events, and stay connected with fellow graduates.

## Features

- User registration and login with session-based authentication
- Profile creation and management
- Alumni directory with search functionality
- Event creation by admin and registration by alumni
- Admin access control
- Flash messages for form validation and user feedback

## Tech Stack

| Component      | Technology        |
|----------------|-------------------|
| Backend        | Python (Flask)    |
| Frontend       | HTML, CSS         |
| Database       | MySQL             |
| Templating     | Jinja2            |
| Authentication | Flask Session     |

## Database Schema

The project uses the following main tables:

- `alumni`: Stores personal, academic, and professional information
- `events`: Event details created by admin users
- `event_registrations`: Event participation records
- `connections`: Social connection requests between alumni
- `news`: Posts shared by alumni for announcements or updates

The SQL schema file is included as `AlumniNetwork.sql`.

## How to Run Locally

1. Clone this repository


