"""
Lead Generation Agent - Main module
"""
from src.api_connectors import LinkedInConnector

class LeadGenerationAgent:
    """Main class for the Lead Generation Agent"""
    
    def __init__(self, config):
        """Initialize the Lead Generation Agent"""
        self.config = config
        self.leads = []
        self.companies = []
        # Initialize connectors
        self.linkedin_connector = LinkedInConnector(config)
    
    def search(self, query="", title=None, company=None, location=None, sources=None):
        """
        Search for leads based on criteria.
        Uses LinkedIn API for real data.
        """
        results = []
        
        # Use LinkedIn connector if included in sources
        if sources and 'linkedin' in sources:
            print(f"Searching LinkedIn with query={query}, title={title}, company={company}, location={location}")
            linkedin_results = self.linkedin_connector.search_people(
                keywords=query,
                title=title,
                company=company,
                location=location
            )
            
            # Transform LinkedIn results to standard format
            for result in linkedin_results:
                lead = {
                    'id': result.get('id', ''),
                    'name': result.get('name', ''),
                    'current_title': result.get('current_title', ''),
                    'current_company': result.get('current_company', ''),
                    'location': result.get('location', ''),
                    'industry': result.get('industry', ''),
                    'linkedin_url': result.get('linkedin_url', ''),
                    'twitter_url': '', # Not available from LinkedIn
                    'score': self._calculate_score(result)
                }
                results.append(lead)
        
        # If no results or no sources specified, fall back to dummy data
        if not results:
            results = [
                {
                    'id': '12345',
                    'name': 'John Doe',
                    'current_title': 'CTO',
                    'current_company': 'Tech Corp',
                    'location': 'San Francisco, CA',
                    'industry': 'Technology',
                    'linkedin_url': 'https://linkedin.com/in/johndoe',
                    'twitter_url': 'https://twitter.com/johndoe',
                    'score': 85
                },
                {
                    'id': '67890',
                    'name': 'Jane Smith',
                    'current_title': 'VP of Engineering',
                    'current_company': 'Software Inc',
                    'location': 'New York, NY',
                    'industry': 'Technology',
                    'linkedin_url': 'https://linkedin.com/in/janesmith',
                    'twitter_url': 'https://twitter.com/janesmith',
                    'score': 78
                },
                {
                    'id': '54321',
                    'name': 'Bob Johnson',
                    'current_title': 'Senior Developer',
                    'current_company': 'Dev Solutions',
                    'location': 'Austin, TX',
                    'industry': 'Technology',
                    'linkedin_url': 'https://linkedin.com/in/bobjohnson',
                    'twitter_url': 'https://twitter.com/bobjohnson',
                    'score': 65
                }
            ]
            print("No results from APIs or no sources specified. Using dummy data.")
            
        return results
    
    def _calculate_score(self, lead_data):
        """Calculate a lead score based on various factors"""
        # Get scoring weights from config
        weights = self.config.get_scoring_settings()
        
        # Start with a base score
        score = 50
        
        # Add points for decision maker roles
        decision_maker_titles = ['CEO', 'CTO', 'CFO', 'COO', 'Director', 'VP', 'Head', 'Chief']
        title = lead_data.get('current_title', '')
        if any(title.startswith(dmt) or dmt in title for dmt in decision_maker_titles):
            score += 20 * weights.get('decision_maker_weight', 0.25)
        
        # Add points for relevant skills
        relevant_skills = ['Leadership', 'Management', 'Strategy', 'Decision Making']
        skills = lead_data.get('skills', [])
        skill_match = sum(1 for skill in skills if any(rs.lower() in skill.lower() for rs in relevant_skills))
        if skills:
            score += (skill_match / len(skills) * 15) * weights.get('skill_relevance_weight', 0.15)
        
        # Clamp score to 0-100 range
        return min(max(int(score), 0), 100)
    
    def get_leads(self, industry=None, company_size=None, status=None):
        """
        Get stored leads with optional filtering.
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
    
    def add_lead(self, lead):
        """
        Add a lead to the stored leads.
        """
        # Check if lead already exists
        for existing_lead in self.leads:
            if existing_lead.get('id') == lead.get('id'):
                return False
        
        # Add lead
        self.leads.append(lead)
        return True
    
    def get_companies(self, industry=None, size=None):
        """
        Get stored companies with optional filtering.
        """
        # Apply filters if provided
        filtered_companies = self.companies
        
        if industry:
            filtered_companies = [company for company in filtered_companies if company.get('industry') == industry]
        
        if size:
            filtered_companies = [company for company in filtered_companies if company.get('size') == size]
        
        return filtered_companies
    
    def generate_suggestions(self, industries=None, company_sizes=None, locations=None, 
                            title_levels=None, min_score=0, max_suggestions=10):
        """
        Generate lead suggestions based on criteria.
        For now, this returns dummy data.
        """
        # In a real implementation, this would use the lead scoring system
        # For now, we'll return dummy suggestions
        return [
            {
                'lead': {
                    'id': '12345',
                    'name': 'John Doe',
                    'current_title': 'CTO',
                    'current_company': 'Tech Corp',
                    'location': 'San Francisco, CA',
                    'industry': 'Technology',
                    'score': 85
                },
                'title': 'High-value tech decision maker',
                'description': 'CTO at growing tech company with decision-making authority',
                'action': 'Reach out with personalized message about enterprise solution',
                'type': 'hot_lead'
            },
            {
                'lead': {
                    'id': '67890',
                    'name': 'Jane Smith',
                    'current_title': 'VP of Engineering',
                    'current_company': 'Software Inc',
                    'location': 'New York, NY',
                    'industry': 'Technology',
                    'score': 78
                },
                'title': 'Engineering leader at established company',
                'description': 'VP of Engineering with influence over technical decisions',
                'action': 'Connect and share case study relevant to their industry',
                'type': 'warm_lead'
            }
        ]
    
    def score_lead(self, lead, target_criteria=None):
        """
        Score a lead based on various factors.
        Returns a score between 0 and 100.
        """
        # In a real implementation, this would use a sophisticated scoring algorithm
        # For now, we'll return a simple score based on title
        if 'CTO' in lead.get('current_title', ''):
            return 85
        elif 'VP' in lead.get('current_title', ''):
            return 78
        elif 'Senior' in lead.get('current_title', ''):
            return 65
        else:
            return 50
