<p align="center">
  <img src="frontend/vayk_frontend/src/assets/navy_logo.png" width="928" height="472" alt="VayK Logo" />
</p>

VayK is a full-stack web application that generates personalized travel itineraries based on user input. Users provide a destination, travel dates, and preferences, and the system produces a curated itinerary by combining external API data with LLM generation.

---

'VayK/frontend/vayk_frontend/src/assets/navy_logo.png'
## Features

- Destination search with dynamic suggestions
- Flexible travel date selection
- Preference-based filtering (e.g., food, outdoors, culture, relaxation)
- AI-generated itineraries using LLM integration
- Interactive and responsive frontend interface
- Backend processing pipeline integrating APIs, database, and LLM

---

## Tech Stack

### Frontend
- Vue.js (Vite)
- JavaScript, HTML, CSS

### Backend
- Django (Python)

### Database
- PostgreSQL

---

## Architecture Overview

The application follows a full-stack workflow:

1. The frontend collects user inputs (destination, dates, preferences)
2. The backend processes requests and manages application logic
3. External APIs provide location and contextual data
4. The database stores relevant information
5. The LLM generates a personalized itinerary
6. The frontend displays the generated results to the user

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Inacio-desouza/VayK.git
cd VayK
git checkout dev
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Mac/Linux
# venv\Scripts\activate    # Windows

pip install -r requirements.txt
```

### 3. Environment Variables

Create a `.env` file in the backend directory:

```env
DB_PASSWORD=your_database_password
```

Ensure this matches your PostgreSQL configuration.

### 4. Run Backend Server

```bash
python manage.py runserver
```

Backend runs at: http://127.0.0.1:8000/

### 5. Frontend Setup

```bash
cd frontend/vayk_frontend
npm install
npm run dev
```

Frontend runs at: http://localhost:5173/

---

## Usage

1. Open the frontend in a browser
2. Enter a destination
3. Select arrival and departure dates
4. Choose travel preferences
5. Generate an itinerary
6. View the recommended activities

---


## Authors

- Samantha Taylormoore
- Inacio de Souza
- Jackson McDonald
- Matthew Pearson

---
## Documents
- [Project proposal](Reports/Project%20Proposal.docx.pdf).
