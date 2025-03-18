"""
Utility for exporting leads to Excel
"""
import os
import time
import pandas as pd

def export_to_excel(leads):
    """
    Export a list of leads to an Excel file
    
    Args:
        leads (list): List of lead dictionaries
        
    Returns:
        str: Filename of the exported Excel file
    """
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
        'linkedin_url', 
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
        
        # Add some formats
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#D7E4BC',
            'border': 1
        })
        
        # Write the column headers with the defined format
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)
            
        # Set column widths
        for i, col in enumerate(df.columns):
            column_len = max(df[col].astype(str).str.len().max(), len(col) + 2)
            worksheet.set_column(i, i, column_len)
    
    return filename 