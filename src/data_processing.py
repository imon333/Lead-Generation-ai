"""
Data processing utilities for the Lead Generation Agent
"""

class DataCleaner:
    """Class for cleaning and normalizing data from different sources"""
    
    def clean_linkedin_data(self, raw_data):
        """
        Clean and normalize LinkedIn data
        
        Args:
            raw_data (dict): Raw data from LinkedIn API
            
        Returns:
            dict: Cleaned and normalized data
        """
        cleaned_data = {
            'name': raw_data.get('fullName', ''),
            'username': raw_data.get('username', ''),
            'current_title': self._extract_title(raw_data.get('headline', '')),
            'current_company': self._extract_company(raw_data.get('headline', '')),
            'location': raw_data.get('location', ''),
            'linkedin_url': raw_data.get('profileURL', ''),
            'skills': raw_data.get('skills', []),
            'experience': raw_data.get('experience', []),
            'source': 'linkedin'
        }
        
        return cleaned_data
    
    def clean_twitter_data(self, raw_data):
        """
        Clean and normalize Twitter data
        
        Args:
            raw_data (dict): Raw data from Twitter API
            
        Returns:
            dict: Cleaned and normalized data
        """
        cleaned_data = {
            'name': raw_data.get('name', ''),
            'username': raw_data.get('screen_name', ''),
            'location': raw_data.get('location', ''),
            'twitter_url': f"https://twitter.com/{raw_data.get('screen_name', '')}",
            'description': raw_data.get('description', ''),
            'tweets': raw_data.get('tweets', []),
            'current_company': self._extract_company_from_bio(raw_data.get('description', '')),
            'current_title': self._extract_title_from_bio(raw_data.get('description', '')),
            'source': 'twitter'
        }
        
        return cleaned_data
    
    def _extract_title(self, headline):
        """Extract job title from headline"""
        if not headline:
            return ''
        
        # Simple extraction - in real implementation, this would be more sophisticated
        if ' at ' in headline:
            return headline.split(' at ')[0].strip()
        return headline
    
    def _extract_company(self, headline):
        """Extract company from headline"""
        if not headline:
            return ''
        
        # Simple extraction - in real implementation, this would be more sophisticated
        if ' at ' in headline:
            return headline.split(' at ')[1].strip()
        return ''
    
    def _extract_company_from_bio(self, bio):
        """Extract company from Twitter bio"""
        if not bio:
            return ''
        
        # Simple extraction - in real implementation, this would be more sophisticated
        if '@' in bio:
            parts = bio.split('@')
            for part in parts[1:]:
                company = part.split()[0].strip()
                if company and not company.startswith(('#', '@')):
                    return company
        
        return ''
    
    def _extract_title_from_bio(self, bio):
        """Extract job title from Twitter bio"""
        if not bio:
            return ''
        
        # Simple extraction - in real implementation, this would be more sophisticated
        common_titles = ['CEO', 'CTO', 'CFO', 'COO', 'VP', 'Director', 'Manager', 'Engineer', 'Developer']
        for title in common_titles:
            if title in bio:
                return title
        
        return ''


class EntityExtractor:
    """Class for extracting entities from cleaned data"""
    
    def extract_entities(self, cleaned_data):
        """
        Extract entities from cleaned data
        
        Args:
            cleaned_data (dict): Cleaned data from DataCleaner
            
        Returns:
            dict: Extracted entities
        """
        entities = {
            'people': [],
            'companies': [],
            'job_titles': [],
            'skills': [],
            'locations': [],
            'hashtags': []
        }
        
        # Extract person
        if cleaned_data.get('name'):
            entities['people'].append({
                'name': cleaned_data.get('name'),
                'username': cleaned_data.get('username'),
                'current_title': cleaned_data.get('current_title'),
                'current_company': cleaned_data.get('current_company')
            })
        
        # Extract company
        if cleaned_data.get('current_company'):
            entities['companies'].append({
                'name': cleaned_data.get('current_company')
            })
        
        # Extract job title
        if cleaned_data.get('current_title'):
            entities['job_titles'].append(cleaned_data.get('current_title'))
        
        # Extract skills
        if cleaned_data.get('skills'):
            entities['skills'].extend(cleaned_data.get('skills'))
        
        # Extract location
        if cleaned_data.get('location'):
            entities['locations'].append(cleaned_data.get('location'))
        
        # Extract hashtags from tweets
        if cleaned_data.get('source') == 'twitter' and cleaned_data.get('tweets'):
            for tweet in cleaned_data.get('tweets'):
                text = tweet.get('text', '')
                hashtags = [word.strip('#') for word in text.split() if word.startswith('#')]
                entities['hashtags'].extend(hashtags)
        
        return entities


class PatternDetector:
    """Class for detecting patterns in data"""
    
    def detect_company_growth_pattern(self, company_data):
        """
        Detect growth pattern for a company
        
        Args:
            company_data (dict): Company data
            
        Returns:
            dict: Growth pattern information
        """
        pattern = {
            'growth_rate': 0,
            'hiring_activity': 'low',
            'growth_stage': 'unknown'
        }
        
        # In a real implementation, this would use sophisticated analysis
        # For now, we'll use simple rules
        
        # Determine growth rate
        if company_data.get('previous_size') and company_data.get('size'):
            prev_size = self._estimate_size(company_data.get('previous_size'))
            curr_size = self._estimate_size(company_data.get('size'))
            
            if prev_size > 0:
                growth_rate = (curr_size - prev_size) / prev_size
                pattern['growth_rate'] = growth_rate
        
        # Determine hiring activity
        job_postings = company_data.get('job_postings', 0)
        recent_hires = company_data.get('recent_hires', 0)
        
        if job_postings > 10 or recent_hires > 5:
            pattern['hiring_activity'] = 'high'
        elif job_postings > 5 or recent_hires > 2:
            pattern['hiring_activity'] = 'medium'
        
        # Determine growth stage
        founded_year = company_data.get('founded')
        size = company_data.get('size')
        
        if founded_year and size:
            current_year = 2025  # Assuming current year
            company_age = current_year - int(founded_year)
            
            if company_age < 3 and self._estimate_size(size) < 50:
                pattern['growth_stage'] = 'startup'
            elif company_age < 7 and self._estimate_size(size) < 200:
                pattern['growth_stage'] = 'scaling'
            else:
                pattern['growth_stage'] = 'established'
        
        return pattern
    
    def detect_skill_trends(self, skills_data):
        """
        Detect trends in skills
        
        Args:
            skills_data (list): List of skill data dictionaries
            
        Returns:
            dict: Skill trends
        """
        trends = {
            'trending_skills': [],
            'declining_skills': [],
            'stable_skills': []
        }
        
        # In a real implementation, this would use sophisticated analysis
        # For now, we'll use simple rules
        
        for skill in skills_data:
            growth_rate = skill.get('growth_rate', 0)
            
            if growth_rate > 0.2:
                trends['trending_skills'].append(skill.get('name'))
            elif growth_rate < -0.1:
                trends['declining_skills'].append(skill.get('name'))
            else:
                trends['stable_skills'].append(skill.get('name'))
        
        return trends
    
    def detect_industry_clusters(self, industry_data):
        """
        Detect clusters in industries
        
        Args:
            industry_data (list): List of industry data dictionaries
            
        Returns:
            dict: Industry clusters
        """
        clusters = {
            'high_growth_industries': [],
            'stable_industries': [],
            'declining_industries': []
        }
        
        # In a real implementation, this would use sophisticated analysis
        # For now, we'll use simple rules
        
        for industry in industry_data:
            growth_rate = industry.get('growth_rate', 0)
            
            if growth_rate > 0.15:
                clusters['high_growth_industries'].append(industry.get('name'))
            elif growth_rate < 0:
                clusters['declining_industries'].append(industry.get('name'))
            else:
                clusters['stable_industries'].append(industry.get('name'))
        
        return clusters
    
    def _estimate_size(self, size_range):
        """Estimate numeric size from size range string"""
        if not size_range:
            return 0
        
        # Handle ranges like "11-50 employees"
        if '-' in size_range:
            parts = size_range.split('-')
            if len(parts) == 2:
                try:
                    min_size = int(parts[0].strip())
                    max_size = int(parts[1].split()[0].strip())
                    return (min_size + max_size) / 2
                except ValueError:
                    pass
        
        # Handle specific numbers
        try:
            return int(size_range.split()[0])
        except (ValueError, IndexError):
            return 0
