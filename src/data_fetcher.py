"""
Data fetcher for the Lead Generation Agent
"""

from src.search_manager import SearchManager
from src.data_processing import DataCleaner, EntityExtractor, PatternDetector
from src.storage_manager import StorageManager

class DataFetcher:
    """Class for fetching and processing data from various sources"""
    
    def __init__(self, config):
        """
        Initialize the DataFetcher
        
        Args:
            config (Config): Configuration object with API settings
        """
        self.config = config
        self.search_manager = SearchManager(config)
        self.data_cleaner = DataCleaner()
        self.entity_extractor = EntityExtractor()
        self.pattern_detector = PatternDetector()
        self.storage_manager = StorageManager()
    
    def fetch_leads(self, query="", title=None, company=None, location=None, sources=None, save=True):
        """
        Fetch leads from various sources
        
        Args:
            query (str): General search query
            title (str): Job title to search for
            company (str): Company to search for
            location (str): Location to search for
            sources (list): List of sources to search (e.g., ['linkedin', 'twitter'])
            save (bool): Whether to save leads to storage
            
        Returns:
            list: Processed lead data
        """
        # Search for leads
        raw_leads = self.search_manager.search(
            query=query,
            title=title,
            company=company,
            location=location,
            sources=sources
        )
        
        # Process leads
        processed_leads = []
        for raw_lead in raw_leads:
            # Clean data based on source
            source = raw_lead.get('source')
            if source == 'linkedin':
                cleaned_lead = self.data_cleaner.clean_linkedin_data(raw_lead)
            elif source == 'twitter':
                cleaned_lead = self.data_cleaner.clean_twitter_data(raw_lead)
            else:
                # Skip leads with unknown source
                continue
            
            # Extract entities
            entities = self.entity_extractor.extract_entities(cleaned_lead)
            
            # Add entities to lead data
            cleaned_lead['entities'] = entities
            
            # Save lead if requested
            if save:
                self.storage_manager.save_lead(cleaned_lead)
            
            processed_leads.append(cleaned_lead)
        
        return processed_leads
    
    def fetch_lead_details(self, lead_id, source):
        """
        Fetch detailed information for a lead
        
        Args:
            lead_id (str): Lead ID
            source (str): Source platform (e.g., 'linkedin', 'twitter')
            
        Returns:
            dict: Detailed lead information
        """
        # Get detailed profile
        raw_profile = self.search_manager.get_profile_details(lead_id, source)
        
        # Clean data based on source
        if source == 'linkedin':
            cleaned_profile = self.data_cleaner.clean_linkedin_data(raw_profile)
        elif source == 'twitter':
            cleaned_profile = self.data_cleaner.clean_twitter_data(raw_profile)
        else:
            raise ValueError(f"Unsupported source: {source}")
        
        # Extract entities
        entities = self.entity_extractor.extract_entities(cleaned_profile)
        
        # Add entities to profile data
        cleaned_profile['entities'] = entities
        
        # Save lead
        self.storage_manager.save_lead(cleaned_profile)
        
        return cleaned_profile
    
    def fetch_company_details(self, company_name, source='linkedin', save=True):
        """
        Fetch detailed information for a company
        
        Args:
            company_name (str): Company name
            source (str): Source platform (default: 'linkedin')
            save (bool): Whether to save company to storage
            
        Returns:
            dict: Detailed company information
        """
        # Get company details
        raw_company = self.search_manager.get_company_details(company_name, source)
        
        # Detect growth pattern
        growth_pattern = self.pattern_detector.detect_company_growth_pattern(raw_company)
        
        # Add growth pattern to company data
        raw_company['growth_pattern'] = growth_pattern
        
        # Save company if requested
        if save:
            self.storage_manager.save_company(raw_company)
        
        return raw_company
    
    def fetch_and_analyze_industry_data(self, industries):
        """
        Fetch and analyze data for multiple industries
        
        Args:
            industries (list): List of industry names
            
        Returns:
            dict: Industry analysis results
        """
        # In a real implementation, this would fetch real data
        # For now, we'll use dummy data
        
        industry_data = []
        for industry in industries:
            industry_data.append({
                'name': industry,
                'companies': 30,  # Dummy value
                'growth_rate': 0.15  # Dummy value
            })
        
        # Detect industry clusters
        clusters = self.pattern_detector.detect_industry_clusters(industry_data)
        
        return {
            'industry_data': industry_data,
            'clusters': clusters
        }
    
    def fetch_and_analyze_skill_data(self, skills):
        """
        Fetch and analyze data for multiple skills
        
        Args:
            skills (list): List of skill names
            
        Returns:
            dict: Skill analysis results
        """
        # In a real implementation, this would fetch real data
        # For now, we'll use dummy data
        
        skill_data = []
        for skill in skills:
            skill_data.append({
                'name': skill,
                'frequency': 100,  # Dummy value
                'growth_rate': 0.1  # Dummy value
            })
        
        # Detect skill trends
        trends = self.pattern_detector.detect_skill_trends(skill_data)
        
        return {
            'skill_data': skill_data,
            'trends': trends
        }
