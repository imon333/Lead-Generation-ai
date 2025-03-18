"""
Lead Generation Web Application
"""
import os
import sys
import json
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS

# Add the parent directory to the path so we can import src modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import Config
from src.lead_generation_agent import LeadGenerationAgent
from app.utils.excel_exporter import export_to_excel

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize configuration and lead generation agent
config = Config()
lead_agent = LeadGenerationAgent(config)

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def search():
    """Search for leads based on criteria"""
    data = request.json
    
    # Extract search parameters
    query = data.get('query', '')
    title = data.get('title')
    company = data.get('company')
    location = data.get('location')
    sources = data.get('sources', ['linkedin'])
    
    # Perform the search
    leads = lead_agent.search(
        query=query,
        title=title,
        company=company,
        location=location,
        sources=sources
    )
    
    return jsonify({"leads": leads})

@app.route('/api/export', methods=['POST'])
def export():
    """Export leads to Excel"""
    data = request.json
    leads = data.get('leads', [])
    
    if not leads:
        return jsonify({"error": "No leads to export"}), 400
    
    # Export to Excel
    filename = export_to_excel(leads)
    
    return jsonify({"filename": filename})

@app.route('/api/download/<filename>')
def download(filename):
    """Download an exported file"""
    file_path = os.path.join(os.getcwd(), 'data', 'exports', filename)
    return send_file(file_path, as_attachment=True)

@app.route('/api/config', methods=['GET'])
def get_config():
    """Get configuration settings"""
    # Only return non-sensitive configuration
    return jsonify({
        "scoring": config.get_scoring_settings()
    })

@app.route('/api/config', methods=['POST'])
def update_config():
    """Update configuration settings"""
    data = request.json
    
    if 'linkedin_api_key' in data:
        config.update_api_settings(linkedin_api_key=data['linkedin_api_key'])
    
    if 'twitter_api_key' in data:
        config.update_api_settings(twitter_api_key=data['twitter_api_key'])
    
    if 'scoring' in data:
        config.update_scoring_settings(data['scoring'])
    
    return jsonify({"success": True})

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs(os.path.join(os.getcwd(), 'data', 'exports'), exist_ok=True)
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000) 