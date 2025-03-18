"""
Main entry point for the Lead Generation application
"""
import os
import sys
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS

from src.config import Config
from src.lead_generation_agent import LeadGenerationAgent

app = Flask(__name__, 
            static_folder='app/static',
            template_folder='app/templates')
CORS(app)  # Enable CORS for all routes

# Initialize configuration and lead generation agent
config = Config()
lead_agent = LeadGenerationAgent(config)

def export_to_excel(leads):
    """
    Export a list of leads to an Excel file
    
    Args:
        leads (list): List of lead dictionaries
        
    Returns:
        str: Filename of the exported Excel file
    """
    import time
    import pandas as pd
    
    # Create a timestamp for the filename
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"leads_export_{timestamp}.xlsx"
    
    # Ensure the exports directory exists
    export_dir = os.path.join(os.getcwd(), 'data', 'exports')
    os.makedirs(export_dir, exist_ok=True)
    
    # Create the full file path
    file_path = os.path.join(export_dir, filename)
    
    # Convert leads to DataFrame
    df = pd.DataFrame(leads)
    
    # Reorder columns for better readability
    columns_order = [
        'name', 
        'current_title', 
        'current_company', 
        'location', 
        'industry', 
        'linkedin_url',  # Ensuring LinkedIn URL is prominent
        'twitter_url', 
        'email',
        'phone', 
        'score'
    ]
    
    # Only use columns that exist in the DataFrame
    available_columns = [col for col in columns_order if col in df.columns]
    # Add any other columns that exist but are not in the columns_order
    remaining_columns = [col for col in df.columns if col not in columns_order]
    final_columns = available_columns + remaining_columns
    
    # Reorder the DataFrame
    df = df[final_columns]
    
    # Export to Excel
    with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Leads', index=False)
        
        # Get the xlsxwriter workbook and worksheet objects
        workbook = writer.book
        worksheet = writer.sheets['Leads']
        
        # Add formats
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#D7E4BC',
            'border': 1
        })
        
        url_format = workbook.add_format({
            'font_color': 'blue',
            'underline': True
        })
        
        # Write the column headers with the defined format
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)
        
        # Format URL columns
        linkedin_col = None
        twitter_col = None
        
        for i, col in enumerate(df.columns):
            if col == 'linkedin_url':
                linkedin_col = i
            elif col == 'twitter_url':
                twitter_col = i
        
        # Apply URL formatting
        if linkedin_col is not None:
            for row_num, url in enumerate(df['linkedin_url']):
                if url and isinstance(url, str) and url.startswith('http'):
                    worksheet.write_url(row_num + 1, linkedin_col, url, url_format, string=url)
        
        if twitter_col is not None:
            for row_num, url in enumerate(df['twitter_url']):
                if url and isinstance(url, str) and url.startswith('http'):
                    worksheet.write_url(row_num + 1, twitter_col, url, url_format, string=url)
            
        # Set column widths
        for i, col in enumerate(df.columns):
            column_len = max(df[col].astype(str).str.len().max(), len(col) + 2)
            worksheet.set_column(i, i, column_len)
    
    return filename

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/simple')
def simple():
    """Render the simple test page"""
    return render_template('simple.html')

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
    
    # Run the app with a different port (8000 instead of 5000)
    app.run(debug=True, host='0.0.0.0', port=8000) 