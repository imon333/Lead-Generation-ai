"""
Feedback processor for the Lead Generation Agent
"""

class FeedbackProcessor:
    """Class for processing user feedback on lead suggestions"""
    
    def __init__(self, config):
        """
        Initialize the FeedbackProcessor
        
        Args:
            config (Config): Configuration object with settings
        """
        self.config = config
        self.feedback_history = []
    
    def process_feedback(self, feedback):
        """
        Process feedback on a lead suggestion
        
        Args:
            feedback (dict): Feedback data
            
        Returns:
            dict: Processed feedback with recommendations
        """
        # Add timestamp
        import datetime
        feedback['timestamp'] = datetime.datetime.now().isoformat()
        
        # Store feedback
        self.feedback_history.append(feedback)
        
        # Generate recommendations based on feedback
        recommendations = self._generate_recommendations(feedback)
        
        # Return processed feedback
        return {
            'original_feedback': feedback,
            'recommendations': recommendations
        }
    
    def _generate_recommendations(self, feedback):
        """
        Generate recommendations based on feedback
        
        Args:
            feedback (dict): Feedback data
            
        Returns:
            list: Recommendations
        """
        recommendations = []
        
        # Extract feedback data
        lead_id = feedback.get('lead_id')
        suggestion_type = feedback.get('suggestion_type')
        rating = feedback.get('rating', 0)  # 1-5 rating
        is_relevant = feedback.get('is_relevant', False)
        comments = feedback.get('comments', '')
        
        # Generate recommendations based on feedback
        if rating >= 4 and is_relevant:
            # Positive feedback
            recommendations.append({
                'type': 'scoring_adjustment',
                'description': 'Increase weight for similar leads',
                'action': 'adjust_scoring_weights',
                'parameters': {
                    'suggestion_type': suggestion_type,
                    'adjustment': 0.1
                }
            })
            
            recommendations.append({
                'type': 'search_recommendation',
                'description': 'Find more leads similar to this one',
                'action': 'search_similar_leads',
                'parameters': {
                    'lead_id': lead_id
                }
            })
            
        elif rating <= 2 or not is_relevant:
            # Negative feedback
            recommendations.append({
                'type': 'scoring_adjustment',
                'description': 'Decrease weight for similar leads',
                'action': 'adjust_scoring_weights',
                'parameters': {
                    'suggestion_type': suggestion_type,
                    'adjustment': -0.1
                }
            })
            
            # Extract keywords from comments for filtering
            keywords = self._extract_keywords_from_comments(comments)
            if keywords:
                recommendations.append({
                    'type': 'filter_recommendation',
                    'description': 'Add filters based on feedback',
                    'action': 'add_filters',
                    'parameters': {
                        'keywords': keywords
                    }
                })
        
        return recommendations
    
    def _extract_keywords_from_comments(self, comments):
        """
        Extract keywords from comments
        
        Args:
            comments (str): User comments
            
        Returns:
            list: Extracted keywords
        """
        # In a real implementation, this would use NLP techniques
        # For now, we'll use a simple approach
        
        if not comments:
            return []
        
        # Convert to lowercase
        comments = comments.lower()
        
        # Look for common feedback phrases
        keywords = []
        
        if 'wrong industry' in comments or 'different industry' in comments:
            keywords.append('industry')
        
        if 'wrong title' in comments or 'not decision maker' in comments:
            keywords.append('title')
        
        if 'wrong location' in comments or 'different region' in comments:
            keywords.append('location')
        
        if 'too small' in comments or 'company size' in comments:
            keywords.append('company_size')
        
        # If no specific keywords found, use general terms
        if not keywords and len(comments.split()) > 3:
            # Just take the first few words as keywords
            keywords = comments.split()[:3]
        
        return keywords
    
    def analyze_feedback_trends(self):
        """
        Analyze trends in feedback history
        
        Returns:
            dict: Feedback trend analysis
        """
        if not self.feedback_history:
            return {
                'average_rating': 0,
                'relevance_rate': 0,
                'common_issues': [],
                'positive_factors': []
            }
        
        # Calculate average rating
        ratings = [feedback.get('rating', 0) for feedback in self.feedback_history]
        average_rating = sum(ratings) / len(ratings) if ratings else 0
        
        # Calculate relevance rate
        relevance_count = sum(1 for feedback in self.feedback_history if feedback.get('is_relevant', False))
        relevance_rate = relevance_count / len(self.feedback_history) if self.feedback_history else 0
        
        # Analyze comments for common issues and positive factors
        all_comments = ' '.join([feedback.get('comments', '') for feedback in self.feedback_history])
        common_issues = self._identify_common_issues(all_comments)
        positive_factors = self._identify_positive_factors(all_comments)
        
        return {
            'average_rating': average_rating,
            'relevance_rate': relevance_rate,
            'common_issues': common_issues,
            'positive_factors': positive_factors
        }
    
    def _identify_common_issues(self, comments):
        """
        Identify common issues from comments
        
        Args:
            comments (str): Combined comments
            
        Returns:
            list: Common issues
        """
        # In a real implementation, this would use NLP techniques
        # For now, we'll use a simple approach
        
        issues = []
        
        if 'wrong industry' in comments.lower():
            issues.append('Industry mismatch')
        
        if 'not decision maker' in comments.lower() or 'wrong title' in comments.lower():
            issues.append('Title/role mismatch')
        
        if 'wrong location' in comments.lower():
            issues.append('Location mismatch')
        
        if 'too small' in comments.lower() or 'company size' in comments.lower():
            issues.append('Company size issues')
        
        if 'irrelevant' in comments.lower() or 'not relevant' in comments.lower():
            issues.append('General relevance issues')
        
        return issues
    
    def _identify_positive_factors(self, comments):
        """
        Identify positive factors from comments
        
        Args:
            comments (str): Combined comments
            
        Returns:
            list: Positive factors
        """
        # In a real implementation, this would use NLP techniques
        # For now, we'll use a simple approach
        
        factors = []
        
        if 'good fit' in comments.lower() or 'great fit' in comments.lower():
            factors.append('Good overall fit')
        
        if 'decision maker' in comments.lower() or 'right title' in comments.lower():
            factors.append('Appropriate decision-maker level')
        
        if 'right industry' in comments.lower() or 'perfect industry' in comments.lower():
            factors.append('Industry match')
        
        if 'right size' in comments.lower() or 'good size' in comments.lower():
            factors.append('Company size match')
        
        if 'relevant' in comments.lower() or 'useful' in comments.lower():
            factors.append('General relevance')
        
        return factors
