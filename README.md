# Lead-Generation-ai

A comprehensive lead generation system that helps businesses identify and qualify potential clients through LinkedIn and other sources.

## Features
- Search for leads based on industry, job title, location, and company
- Score and rank potential leads
- Export leads to Excel format
- Web-based UI for easy interaction
- Integration with LinkedIn API (requires API credentials)

## Project Structure
- `/app` - Web application with Flask backend and React frontend
- `/src` - Core lead generation engine and utilities
- `/data` - Local data storage
- `/docs` - Documentation
- `/notebooks` - Jupyter notebooks for analysis

## Setup
1. Clone the repository
2. Install backend dependencies: `pip install -r requirements.txt`
3. Install frontend dependencies: `cd app/frontend && npm install`
4. Configure API credentials in `src/config.py`
5. Run the application: `python app/app.py`

## Usage
1. Access the web interface at http://localhost:5000
2. Enter search criteria for leads
3. View and filter results
4. Export selected leads to Excel