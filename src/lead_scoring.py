"""
Lead scoring and ranking utilities for the Lead Generation Agent
"""

class LeadScorer:
    """Class for scoring leads based on various factors"""
    
    def __init__(self, scoring_settings=None):
        """
        Initialize the LeadScorer
        
        Args:
            scoring_settings (dict): Weights for different scoring factors
        """
        self.scoring_settings = scoring_settings or {
            'decision_maker_weight': 0.25,
            'company_fit_weight': 0.20,
            'growth_potential_weight': 0.15,
            'skill_relevance_weight': 0.15,
            'location_relevance_weight': 0.10,
            'engagement_potential_weight': 0.15
        }
    
    def calculate_score(self, lead, target_criteria=None):
        """
        Calculate overall score for a lead
        
        Args:
            lead (dict): Lead data
            target_criteria (dict): Target criteria for scoring
            
        Returns:
            tuple: (score, score_components)
        """
        target_criteria = target_criteria or {}
        
        # Calculate individual component scores
        decision_maker_score = self.score_decision_maker(lead)
        company_fit_score = self.score_company_fit(lead, target_criteria)
        growth_potential_score = self.score_growth_potential(lead)
        skill_relevance_score = self.score_skill_relevance(lead, target_criteria)
        location_relevance_score = self.score_location_relevance(lead, target_criteria)
        engagement_potential_score = self.score_engagement_potential(lead)
        
        # Calculate weighted score
        weighted_score = (
            decision_maker_score * self.scoring_settings['decision_maker_weight'] +
            company_fit_score * self.scoring_settings['company_fit_weight'] +
            growth_potential_score * self.scoring_settings['growth_potential_weight'] +
            skill_relevance_score * self.scoring_settings['skill_relevance_weight'] +
            location_relevance_score * self.scoring_settings['location_relevance_weight'] +
            engagement_potential_score * self.scoring_settings['engagement_potential_weight']
        )
        
        # Scale to 0-100
        final_score = int(weighted_score * 100)
        
        # Prepare score components
        score_components = {
            'decision_maker': decision_maker_score,
            'company_fit': company_fit_score,
            'growth_potential': growth_potential_score,
            'skill_relevance': skill_relevance_score,
            'location_relevance': location_relevance_score,
            'engagement_potential': engagement_potential_score
        }
        
        return final_score, score_components
    
    def score_decision_maker(self, lead):
        """
        Score lead based on decision maker status
        
        Args:
            lead (dict): Lead data
            
        Returns:
            float: Score between 0 and 1
        """
        # In a real implementation, this would use more sophisticated analysis
        # For now, we'll use simple rules based on title
        
        title = lead.get('current_title', '').lower()
        
        # C-level executives
        if any(prefix in title for prefix in ['ceo', 'cto', 'cio', 'cfo', 'coo', 'chief']):
            return 1.0
        
        # VPs and Directors
        if any(prefix in title for prefix in ['vp', 'vice president', 'director']):
            return 0.8
        
        # Managers
        if 'manager' in title or 'head of' in title:
            return 0.6
        
        # Senior individual contributors
        if any(prefix in title for prefix in ['senior', 'lead', 'principal']):
            return 0.4
        
        # Other individual contributors
        return 0.2
    
    def score_company_fit(self, lead, target_criteria):
        """
        Score lead based on company fit
        
        Args:
            lead (dict): Lead data
            target_criteria (dict): Target criteria for scoring
            
        Returns:
            float: Score between 0 and 1
        """
        score = 0.5  # Default score
        
        # Industry match
        if 'industries' in target_criteria and lead.get('industry'):
            if lead.get('industry') in target_criteria['industries']:
                score += 0.2
        
        # Company size match
        if 'company_sizes' in target_criteria and lead.get('company_size'):
            if lead.get('company_size') in target_criteria['company_sizes']:
                score += 0.2
        
        # Cap score at 1.0
        return min(score, 1.0)
    
    def score_growth_potential(self, lead):
        """
        Score lead based on growth potential
        
        Args:
            lead (dict): Lead data
            
        Returns:
            float: Score between 0 and 1
        """
        # In a real implementation, this would use more sophisticated analysis
        # For now, we'll return a default score
        return 0.7
    
    def score_skill_relevance(self, lead, target_criteria):
        """
        Score lead based on skill relevance
        
        Args:
            lead (dict): Lead data
            target_criteria (dict): Target criteria for scoring
            
        Returns:
            float: Score between 0 and 1
        """
        if 'skills' not in target_criteria or not lead.get('skills'):
            return 0.5  # Default score
        
        # Calculate skill match ratio
        target_skills = set(target_criteria['skills'])
        lead_skills = set(lead.get('skills', []))
        
        if not target_skills:
            return 0.5
        
        # Calculate intersection
        matching_skills = target_skills.intersection(lead_skills)
        match_ratio = len(matching_skills) / len(target_skills)
        
        # Scale to 0-1
        return min(match_ratio, 1.0)
    
    def score_location_relevance(self, lead, target_criteria):
        """
        Score lead based on location relevance
        
        Args:
            lead (dict): Lead data
            target_criteria (dict): Target criteria for scoring
            
        Returns:
            float: Score between 0 and 1
        """
        if 'locations' not in target_criteria or not lead.get('location'):
            return 0.5  # Default score
        
        # Check if location matches any target location
        lead_location = lead.get('location', '').lower()
        
        for target_location in target_criteria['locations']:
            if target_location.lower() in lead_location or lead_location in target_location.lower():
                return 1.0
        
        # No match
        return 0.3
    
    def score_engagement_potential(self, lead):
        """
        Score lead based on engagement potential
        
        Args:
            lead (dict): Lead data
            
        Returns:
            float: Score between 0 and 1
        """
        # In a real implementation, this would analyze activity, connections, etc.
        # For now, we'll use engagement signals if available
        
        engagement_signals = lead.get('engagement_signals', [])
        
        if not engagement_signals:
            return 0.5  # Default score
        
        # More signals = higher score
        signal_count = len(engagement_signals)
        
        if signal_count >= 3:
            return 1.0
        elif signal_count == 2:
            return 0.8
        elif signal_count == 1:
            return 0.6
        else:
            return 0.5


class LeadRanker:
    """Class for ranking leads based on scores"""
    
    def rank_leads(self, leads):
        """
        Rank leads by score
        
        Args:
            leads (list): List of lead dictionaries with scores
            
        Returns:
            list: Ranked leads
        """
        # Sort leads by score in descending order
        return sorted(leads, key=lambda x: x.get('score', 0), reverse=True)
    
    def filter_leads_by_score(self, leads, min_score=0):
        """
        Filter leads by minimum score
        
        Args:
            leads (list): List of lead dictionaries with scores
            min_score (int): Minimum score threshold
            
        Returns:
            list: Filtered leads
        """
        return [lead for lead in leads if lead.get('score', 0) >= min_score]
    
    def categorize_leads(self, leads):
        """
        Categorize leads as hot, warm, or cold based on score
        
        Args:
            leads (list): List of lead dictionaries with scores
            
        Returns:
            dict: Categorized leads
        """
        categorized = {
            'hot': [],
            'warm': [],
            'cold': []
        }
        
        for lead in leads:
            score = lead.get('score', 0)
            
            if score >= 80:
                categorized['hot'].append(lead)
            elif score >= 60:
                categorized['warm'].append(lead)
            else:
                categorized['cold'].append(lead)
        
        return categorized
