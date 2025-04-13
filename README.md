# Fullstack Developer Capstone Project

A fullstack car dealership management web application built with Django and React.

## Features

- User authentication (login, logout, register)
- View dealership information
- Team information page
- Contact form

## Technologies Used

- **Backend**: Django
- **Frontend**: React
- **Database**: SQLite
- **Styling**: CSS, Bootstrap

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/fullstack_developer_capstone.git
   cd fullstack_developer_capstone
   ```

2. Set up the backend:
   ```
   cd server
   pip install -r requirements.txt
   python manage.py migrate
   ```

3. Set up the frontend:
   ```
   cd frontend
   npm install
   npm run build
   ```

4. Start the development server:
   ```
   cd ..
   python manage.py runserver
   ```

5. Visit `http://127.0.0.1:8000` in your browser.

## Project Structure

- `server/`: Django backend
  - `djangoapp/`: Main Django application
  - `templates/`: HTML templates
  - `static/`: Static files
  - `frontend/`: React frontend
    - `src/`: React source code
    - `build/`: Compiled React code

## License

This project is licensed under the MIT License - see the LICENSE file for details.