# College Calendar

A simple web-based calendar application for managing college events and assignments.

## Description

This project is a college assignment that implements a calendar management system with a FastAPI backend and interactive frontend. Users can add, edit, and delete events with color-coding support.

## Features

- Add events with title, date, time, and description
- Color-code events for better organization
- Edit existing events
- Delete events
- MongoDB database for persistent storage
- Responsive web interface

## Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: MongoDB
- **Frontend**: HTML, CSS, JavaScript

## Installation

1. Clone the repository:
```bash
git clone https://github.com/akxgami/college_calendar.git
cd college_calendar
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up MongoDB:
   - Install MongoDB locally or use a cloud instance
   - Set the `MONGO_URI` environment variable (defaults to `mongodb://localhost:27017`)

## Usage

Run the application:
```bash
uvicorn main:app --reload
```

Access the calendar at `http://localhost:8000`

## API Endpoints

- `GET /` - Serve the calendar interface
- `GET /events` - Fetch all events
- `POST /events` - Create a new event
- `PUT /events/{id}` - Update an event
- `DELETE /events/{id}` - Delete an event

## Project Structure

```
college_calendar/
├── main.py           # FastAPI backend
├── index.html        # Frontend interface
├── requirements.txt  # Python dependencies
└── README.md         # Documentation
```

## Assignment Details

**Course**: [Your Course Name]  
**Submitted by**: [Your Name]  
**Date**: October 2026

## License

This project is submitted as a college assignment.
