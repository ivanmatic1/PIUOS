# Blog Application with Django Rest and Angular TS

This is a simple blog application built using Django Rest Framework for the backend API and Angular with TypeScript for the frontend.

## Features

- Users can view blog posts.
- Users can create an account and log in.
- Authenticated users can create, edit, and delete their own blog posts.
- Users can like and comment on blog posts.
- Users can search for specific blogs and categorize blogs to see only specific categories of blogs.

## Installation

### Backend

1. Clone this repository.
2. Navigate to the `PIUOS` directory.
3. Create a virtual environment: python -m venv venv
4. Activate the virtual environment:
	- On Windows: `venv\Scripts\activate`
	- On macOS and Linux: `source venv/bin/activate`
5. Install dependencies:
	- Django
	- Django REST Framework
	- django-cors-headers
	- django-filter
	- djangorestframework-jwt
	- markdown
6. Run the server: python manage.py runserver

### Frontend

1. Navigate to the `frontend` directory.
2. Install dependencies: npm install
3. Run the development server: ng serve

## Usage

- Visit `http://localhost:4200` to access the frontend.
- The backend API endpoints are available at `http://localhost:8000/api/`.

## License

This project is licensed under the [MIT License](LICENSE).
