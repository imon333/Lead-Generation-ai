"""
Configuration module for the Lead Generation Agent
"""

class Config:
    """Configuration class for the Lead Generation Agent"""
    
    def __init__(self):
        """Initialize configuration with default values"""
        self.api_settings = {
            'linkedin_api_key': '',
            'twitter_api_key': 'your_twitter_api_key'
        }
        
        self.scoring_settings = {
            'decision_maker_weight': 0.25,
            'company_fit_weight': 0.20,
            'growth_potential_weight': 0.15,
            'skill_relevance_weight': 0.15,
            'location_relevance_weight': 0.10,
            'engagement_potential_weight': 0.15
        }
        
    def get_api_settings(self):
        """Get API settings"""
        return self.api_settings
    
    def get_scoring_settings(self):
        """Get scoring settings"""
        return self.scoring_settings
    
    def update_api_settings(self, linkedin_api_key=None, twitter_api_key=None):
        """Update API settings"""
        if linkedin_api_key:
            self.api_settings['linkedin_api_key'] = linkedin_api_key
        if twitter_api_key:
            self.api_settings['twitter_api_key'] = twitter_api_key
        return True
    
    def update_scoring_settings(self, new_settings):
        """Update scoring settings"""
        self.scoring_settings.update(new_settings)
        return True
