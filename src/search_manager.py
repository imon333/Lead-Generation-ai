"""
Search manager for the Lead Generation Agent
"""

from src.api_connectors import LinkedInConnector, TwitterConnector

class SearchManager:
    """Class for managing search operations across different sources"""
    
    def __init__(self, config):
        """
        Initialize the SearchManager
        
        Args:
            config (Config): Configuration object with API settings
        """
        self.config = config
        self.linkedin_connector = LinkedInConnector(config)
        self.twitter_connector = TwitterConnector(config)
    
    def search(self, query="", title=None, company=None, location=None, sources=None):
        """
        Search for leads across different sources
        
        Args:
            query (str): General search query
            title (str): Job title to search for
            company (str): Company to search for
            location (str): Location to search for
            sources (list): List of sources to search (e.g., ['linkedin', 'twitter'])
            
        Returns:
            list: Combined search results from all sources
        """
        # Default to all sources if not specified
        if sources is None:
            sources = ['linkedin', 'twitter']
        
        results = []
        
        # Search LinkedIn
        if 'linkedin' in sources:
            linkedin_results = self.search_linkedin(query, title, company, location)
            results.extend(linkedin_results)
        
        # Search Twitter
        if 'twitter' in sources:
            twitter_results = self.search_twitter(query, title, company, location)
            results.extend(twitter_results)
        
        # Remove duplicates (in a real implementation, this would be more sophisticated)
        # For now, we'll just use the ID as a unique identifier
        unique_results = {}
        for result in results:
            unique_results[result.get('id')] = result
        
        return list(unique_results.values())
    
    def search_linkedin(self, query="", title=None, company=None, location=None):
        """
        Search for leads on LinkedIn
        
        Args:
            query (str): General search query
            title (str): Job title to search for
            company (str): Company to search for
            location (str): Location to search for
            
        Returns:
            list: LinkedIn search results
        """
        # Prepare search parameters
        keywords = query
        if title:
            keywords = f"{keywords} {title}" if keywords else title
        
        # Search LinkedIn
        return self.linkedin_connector.search_people(
            keywords=keywords,
            title=title,
            company=company,
            location=location
        )
    
    def search_twitter(self, query="", title=None, company=None, location=None):
        """
        Search for leads on Twitter
        
        Args:
            query (str): General search query
            title (str): Job title to search for
            company (str): Company to search for
            location (str): Location to search for
            
        Returns:
            list: Twitter search results
        """
        # Prepare search query
        search_query = query
        if title:
            search_query = f"{search_query} {title}" if search_query else title
        if company:
            search_query = f"{search_query} {company}" if search_query else company
        if location:
            search_query = f"{search_query} {location}" if search_query else location
        
        # Search Twitter
        return self.twitter_connector.search_users(search_query)
    
    def get_profile_details(self, lead_id, source):
        """
        Get detailed profile information for a lead
        
        Args:
            lead_id (str): Lead ID
            source (str): Source platform (e.g., 'linkedin', 'twitter')
            
        Returns:
            dict: Detailed profile information
        """
        if source == 'linkedin':
            # Extract username from lead_id or LinkedIn URL
            username = lead_id.replace('linkedin-', '')
            return self.linkedin_connector.get_profile(username)
        
        elif source == 'twitter':
            # Extract username from lead_id or Twitter URL
            username = lead_id.replace('twitter-', '')
            user_data = self.twitter_connector.get_user(username)
            
            # Get tweets for additional information
            tweets = self.twitter_connector.get_tweets(username)
            user_data['tweets'] = tweets
            
            return user_data
        
        else:
            raise ValueError(f"Unsupported source: {source}")
    
    def get_company_details(self, company_name, source='linkedin'):
        """
        Get detailed company information
        
        Args:
            company_name (str): Company name
            source (str): Source platform (default: 'linkedin')
            
        Returns:
            dict: Detailed company information
        """
        if source == 'linkedin':
            return self.linkedin_connector.get_company(company_name)
        else:
            raise ValueError(f"Unsupported source for company details: {source}")
