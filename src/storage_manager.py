"""
Storage manager for the Lead Generation Agent
"""

import json
import os
import pandas as pd

class StorageManager:
    """Class for managing data storage for the Lead Generation Agent"""
    
    def __init__(self, data_dir='data'):
        """
        Initialize the StorageManager
        
        Args:
            data_dir (str): Directory for storing data
        """
        self.data_dir = data_dir
        self.leads = []
        self.companies = []
        self.feedback = []
        
        # Create data directory if it doesn't exist
        os.makedirs(self.data_dir, exist_ok=True)
    
    def save_lead(self, lead):
        """
        Save a lead to storage
        
        Args:
            lead (dict): Lead data
            
        Returns:
            bool: Success status
        """
        # Check if lead already exists
        for i, existing_lead in enumerate(self.leads):
            if existing_lead.get('id') == lead.get('id'):
                # Update existing lead
                self.leads[i] = lead
                return True
        
        # Add new lead
        self.leads.append(lead)
        return True
    
    def get_leads(self, industry=None, company_size=None, status=None):
        """
        Get leads with optional filtering
        
        Args:
            industry (str): Filter by industry
            company_size (str): Filter by company size
            status (str): Filter by status
            
        Returns:
            list: Filtered leads
        """
        # Apply filters if provided
        filtered_leads = self.leads
        
        if industry:
            filtered_leads = [lead for lead in filtered_leads if lead.get('industry') == industry]
        
        if company_size:
            filtered_leads = [lead for lead in filtered_leads if lead.get('company_size') == company_size]
        
        if status:
            filtered_leads = [lead for lead in filtered_leads if lead.get('status') == status]
        
        return filtered_leads
    
    def get_lead_by_id(self, lead_id):
        """
        Get lead by ID
        
        Args:
            lead_id (str): Lead ID
            
        Returns:
            dict: Lead data or None if not found
        """
        for lead in self.leads:
            if lead.get('id') == lead_id:
                return lead
        return None
    
    def update_lead(self, lead_id, updates):
        """
        Update lead data
        
        Args:
            lead_id (str): Lead ID
            updates (dict): Updates to apply
            
        Returns:
            bool: Success status
        """
        for i, lead in enumerate(self.leads):
            if lead.get('id') == lead_id:
                # Apply updates
                self.leads[i].update(updates)
                return True
        return False
    
    def delete_lead(self, lead_id):
        """
        Delete lead by ID
        
        Args:
            lead_id (str): Lead ID
            
        Returns:
            bool: Success status
        """
        for i, lead in enumerate(self.leads):
            if lead.get('id') == lead_id:
                del self.leads[i]
                return True
        return False
    
    def save_company(self, company):
        """
        Save a company to storage
        
        Args:
            company (dict): Company data
            
        Returns:
            bool: Success status
        """
        # Check if company already exists
        for i, existing_company in enumerate(self.companies):
            if existing_company.get('id') == company.get('id'):
                # Update existing company
                self.companies[i] = company
                return True
        
        # Add new company
        self.companies.append(company)
        return True
    
    def get_companies(self, industry=None, size=None):
        """
        Get companies with optional filtering
        
        Args:
            industry (str): Filter by industry
            size (str): Filter by size
            
        Returns:
            list: Filtered companies
        """
        # Apply filters if provided
        filtered_companies = self.companies
        
        if industry:
            filtered_companies = [company for company in filtered_companies if company.get('industry') == industry]
        
        if size:
            filtered_companies = [company for company in filtered_companies if company.get('size') == size]
        
        return filtered_companies
    
    def get_company_by_id(self, company_id):
        """
        Get company by ID
        
        Args:
            company_id (str): Company ID
            
        Returns:
            dict: Company data or None if not found
        """
        for company in self.companies:
            if company.get('id') == company_id:
                return company
        return None
    
    def save_feedback(self, feedback):
        """
        Save feedback to storage
        
        Args:
            feedback (dict): Feedback data
            
        Returns:
            bool: Success status
        """
        self.feedback.append(feedback)
        return True
    
    def get_all_feedback(self):
        """
        Get all feedback
        
        Returns:
            list: All feedback
        """
        return self.feedback
    
    def export_to_csv(self, data_type, filename=None):
        """
        Export data to CSV
        
        Args:
            data_type (str): Type of data to export ('leads', 'companies', or 'feedback')
            filename (str): Output filename (optional)
            
        Returns:
            str: Path to the exported file
        """
        if data_type == 'leads':
            data = self.leads
            default_filename = 'leads.csv'
        elif data_type == 'companies':
            data = self.companies
            default_filename = 'companies.csv'
        elif data_type == 'feedback':
            data = self.feedback
            default_filename = 'feedback.csv'
        else:
            raise ValueError(f"Unsupported data type: {data_type}")
        
        # Use default filename if not provided
        if filename is None:
            filename = default_filename
        
        # Create full path
        filepath = os.path.join(self.data_dir, filename)
        
        # Convert to DataFrame and save
        df = pd.DataFrame(data)
        df.to_csv(filepath, index=False)
        
        return filepath
    
    def import_from_csv(self, data_type, filepath):
        """
        Import data from CSV
        
        Args:
            data_type (str): Type of data to import ('leads', 'companies', or 'feedback')
            filepath (str): Path to the CSV file
            
        Returns:
            bool: Success status
        """
        try:
            # Read CSV
            df = pd.read_csv(filepath)
            data = df.to_dict('records')
            
            # Import data
            if data_type == 'leads':
                self.leads = data
            elif data_type == 'companies':
                self.companies = data
            elif data_type == 'feedback':
                self.feedback = data
            else:
                raise ValueError(f"Unsupported data type: {data_type}")
            
            return True
        except Exception as e:
            print(f"Error importing data: {e}")
            return False
    
    def export_to_json(self, data_type, filename=None):
        """
        Export data to JSON
        
        Args:
            data_type (str): Type of data to export ('leads', 'companies', 'feedback', or 'all')
            filename (str): Output filename (optional)
            
        Returns:
            str: Path to the exported file
        """
        if data_type == 'leads':
            data = self.leads
            default_filename = 'leads.json'
        elif data_type == 'companies':
            data = self.companies
            default_filename = 'companies.json'
        elif data_type == 'feedback':
            data = self.feedback
            default_filename = 'feedback.json'
        elif data_type == 'all':
            data = {
                'leads': self.leads,
                'companies': self.companies,
                'feedback': self.feedback
            }
            default_filename = 'all_data.json'
        else:
            raise ValueError(f"Unsupported data type: {data_type}")
        
        # Use default filename if not provided
        if filename is None:
            filename = default_filename
        
        # Create full path
        filepath = os.path.join(self.data_dir, filename)
        
        # Save to JSON
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        return filepath
    
    def import_from_json(self, data_type, filepath):
        """
        Import data from JSON
        
        Args:
            data_type (str): Type of data to import ('leads', 'companies', 'feedback', or 'all')
            filepath (str): Path to the JSON file
            
        Returns:
            bool: Success status
        """
        try:
            # Read JSON
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            # Import data
            if data_type == 'leads':
                self.leads = data
            elif data_type == 'companies':
                self.companies = data
            elif data_type == 'feedback':
                self.feedback = data
            elif data_type == 'all':
                self.leads = data.get('leads', [])
                self.companies = data.get('companies', [])
                self.feedback = data.get('feedback', [])
            else:
                raise ValueError(f"Unsupported data type: {data_type}")
            
            return True
        except Exception as e:
            print(f"Error importing data: {e}")
            return False
    
    def get_database_stats(self):
        """
        Get database statistics
        
        Returns:
            dict: Database statistics
        """
        return {
            'total_leads': len(self.leads),
            'total_companies': len(self.companies),
            'total_feedback': len(self.feedback)
        }
    
    def clear_database(self, data_type=None):
        """
        Clear database
        
        Args:
            data_type (str): Type of data to clear ('leads', 'companies', 'feedback', or None for all)
            
        Returns:
            bool: Success status
        """
        if data_type == 'leads':
            self.leads = []
        elif data_type == 'companies':
            self.companies = []
        elif data_type == 'feedback':
            self.feedback = []
        elif data_type is None:
            self.leads = []
            self.companies = []
            self.feedback = []
        else:
            raise ValueError(f"Unsupported data type: {data_type}")
        
        return True
