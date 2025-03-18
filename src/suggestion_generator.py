"""
Suggestion generator for the Lead Generation Agent
"""

from src.lead_scoring import LeadScorer, LeadRanker

class SuggestionGenerator:
    """Class for generating lead suggestions"""
    
    def __init__(self, config):
        """
        Initialize the SuggestionGenerator
        
        Args:
            config (Config): Configuration object with settings
        """
        self.config = config
        self.lead_scorer = LeadScorer(config.get_scoring_settings())
        self.lead_ranker = LeadRanker()
    
    def generate_suggestions(self, leads, target_criteria=None, min_score=0, max_suggestions=10):
        """
        Generate lead suggestions based on criteria
        
        Args:
            leads (list): List of lead dictionaries
            target_criteria (dict): Target criteria for scoring
            min_score (int): Minimum score threshold
            max_suggestions (int): Maximum number of suggestions to generate
            
        Returns:
            list: Lead suggestions
        """
        # Score leads if they don't have scores
        scored_leads = []
        for lead in leads:
            if 'score' not in lead or 'score_components' not in lead:
                score, score_components = self.lead_scorer.calculate_score(lead, target_criteria)
                lead['score'] = score
                lead['score_components'] = score_components
            scored_leads.append(lead)
        
        # Filter by minimum score
        filtered_leads = [lead for lead in scored_leads if lead.get('score', 0) >= min_score]
        
        # Rank leads
        ranked_leads = self.lead_ranker.rank_leads(filtered_leads)
        
        # Limit to max_suggestions
        top_leads = ranked_leads[:max_suggestions]
        
        # Generate suggestions
        suggestions = []
        for lead in top_leads:
            suggestion = self._create_suggestion(lead)
            suggestions.append(suggestion)
        
        return suggestions
    
    def _create_suggestion(self, lead):
        """
        Create a suggestion for a lead
        
        Args:
            lead (dict): Lead dictionary with score and score_components
            
        Returns:
            dict: Suggestion
        """
        # Determine suggestion type based on score
        score = lead.get('score', 0)
        if score >= 80:
            suggestion_type = 'hot_lead'
        elif score >= 60:
            suggestion_type = 'warm_lead'
        else:
            suggestion_type = 'cold_lead'
        
        # Create title based on lead characteristics
        title = self._generate_title(lead, suggestion_type)
        
        # Create description based on lead characteristics
        description = self._generate_description(lead, suggestion_type)
        
        # Create action recommendation
        action = self._generate_action(lead, suggestion_type)
        
        return {
            'lead': lead,
            'title': title,
            'description': description,
            'action': action,
            'type': suggestion_type
        }
    
    def _generate_title(self, lead, suggestion_type):
        """
        Generate a title for a suggestion
        
        Args:
            lead (dict): Lead dictionary
            suggestion_type (str): Suggestion type
            
        Returns:
            str: Suggestion title
        """
        name = lead.get('name', '')
        title = lead.get('current_title', '')
        company = lead.get('current_company', '')
        industry = lead.get('industry', '')
        
        if suggestion_type == 'hot_lead':
            if 'C' in title or 'Chief' in title:
                return f"High-value executive decision maker at {company}"
            else:
                return f"High-potential lead in {industry} industry"
        
        elif suggestion_type == 'warm_lead':
            return f"Promising {title} at {company}"
        
        else:
            return f"Potential lead: {name}, {title}"
    
    def _generate_description(self, lead, suggestion_type):
        """
        Generate a description for a suggestion
        
        Args:
            lead (dict): Lead dictionary
            suggestion_type (str): Suggestion type
            
        Returns:
            str: Suggestion description
        """
        name = lead.get('name', '')
        title = lead.get('current_title', '')
        company = lead.get('current_company', '')
        location = lead.get('location', '')
        score = lead.get('score', 0)
        score_components = lead.get('score_components', {})
        
        # Identify top strengths
        strengths = []
        if score_components.get('decision_maker', 0) >= 0.8:
            strengths.append("decision-making authority")
        if score_components.get('company_fit', 0) >= 0.8:
            strengths.append("strong company fit")
        if score_components.get('growth_potential', 0) >= 0.8:
            strengths.append("high growth potential")
        if score_components.get('skill_relevance', 0) >= 0.8:
            strengths.append("relevant skill set")
        if score_components.get('location_relevance', 0) >= 0.8:
            strengths.append("ideal location")
        if score_components.get('engagement_potential', 0) >= 0.8:
            strengths.append("high engagement potential")
        
        strengths_text = ""
        if strengths:
            if len(strengths) == 1:
                strengths_text = f" with {strengths[0]}"
            elif len(strengths) == 2:
                strengths_text = f" with {strengths[0]} and {strengths[1]}"
            else:
                strengths_text = f" with {', '.join(strengths[:-1])}, and {strengths[-1]}"
        
        if suggestion_type == 'hot_lead':
            return f"{name} is a {title} at {company} based in {location}{strengths_text}. With a lead score of {score}, they represent a high-value opportunity."
        
        elif suggestion_type == 'warm_lead':
            return f"{name} is a {title} at {company} based in {location}{strengths_text}. Their lead score of {score} indicates good potential."
        
        else:
            return f"{name} is a {title} at {company} based in {location}. Their lead score is {score}."
    
    def _generate_action(self, lead, suggestion_type):
        """
        Generate an action recommendation for a suggestion
        
        Args:
            lead (dict): Lead dictionary
            suggestion_type (str): Suggestion type
            
        Returns:
            str: Action recommendation
        """
        name = lead.get('name', '')
        title = lead.get('current_title', '')
        company = lead.get('current_company', '')
        
        if suggestion_type == 'hot_lead':
            return f"Reach out directly with a personalized message highlighting specific value propositions for {company}."
        
        elif suggestion_type == 'warm_lead':
            return f"Connect on LinkedIn with a personalized invitation and share relevant content to establish credibility."
        
        else:
            return f"Add to nurture campaign and monitor for engagement signals before direct outreach."
