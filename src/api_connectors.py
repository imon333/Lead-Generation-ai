"""
API connector utilities for the Lead Generation Agent
"""
import requests
import json
import random
import time

class LinkedInConnector:
    """Class for connecting to LinkedIn API"""
    
    def __init__(self, config):
        """
        Initialize the LinkedIn connector
        
        Args:
            config (Config): Configuration object with API settings
        """
        self.api_key = config.get_api_settings().get('linkedin_api_key')
        self.base_url = "https://api.linkedin.com/v2"
        
    def search_people(self, keywords=None, first_name=None, last_name=None, title=None, company=None, school=None, location=None, industry=None):
        """
        Search for people on LinkedIn
        
        Args:
            keywords (str): Keywords to search for
            first_name (str): First name to search for
            last_name (str): Last name to search for
            title (str): Job title to search for
            company (str): Company to search for
            school (str): School to search for
            location (str): Location to search for
            industry (str): Industry to search for
            
        Returns:
            list: List of people matching the search criteria
        """
        # Log the search parameters
        print(f"Searching LinkedIn for people with parameters: keywords={keywords}, title={title}, company={company}, location={location}")
        
        # Check if API key is available
        if not self.api_key or self.api_key == 'your_linkedin_api_key':
            print("No valid LinkedIn API key found. Using dummy data.")
            return self._get_dummy_data(keywords, title, company, location)
        
        try:
            # Construct the search URL and parameters
            search_url = f"{self.base_url}/people-search"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            params = {}
            
            # Add search parameters if provided
            if keywords:
                params["keywords"] = keywords
            if title:
                params["title"] = title
            if company:
                params["company_name"] = company
            if location:
                params["location"] = location
            if first_name:
                params["first_name"] = first_name
            if last_name:
                params["last_name"] = last_name
            if industry:
                params["industry"] = industry
                
            # Make the API request
            response = requests.get(search_url, headers=headers, params=params)
            
            # Check if the request was successful
            if response.status_code == 200:
                data = response.json()
                return self._process_linkedin_response(data)
            else:
                print(f"LinkedIn API request failed with status code {response.status_code}")
                print(f"Response: {response.text}")
                return self._get_dummy_data(keywords, title, company, location)
                
        except Exception as e:
            print(f"Error connecting to LinkedIn API: {str(e)}")
            return self._get_dummy_data(keywords, title, company, location)
    
    def _process_linkedin_response(self, data):
        """Process the response from LinkedIn API"""
        results = []
        
        # Extract the people from the response
        # The actual data structure depends on the LinkedIn API response format
        people = data.get("elements", [])
        
        for person in people:
            # Extract relevant information
            person_data = {
                "id": person.get("id", ""),
                "name": f"{person.get('firstName', '')} {person.get('lastName', '')}",
                "current_title": person.get("headline", ""),
                "current_company": self._extract_company(person),
                "location": person.get("location", {}).get("name", ""),
                "industry": person.get("industry", ""),
                "linkedin_url": f"https://linkedin.com/in/{person.get('vanityName', '')}",
                "skills": self._extract_skills(person)
            }
            results.append(person_data)
            
        return results
    
    def _extract_company(self, person):
        """Extract the current company from a person's profile"""
        positions = person.get("positions", {}).get("elements", [])
        if positions and len(positions) > 0:
            current_position = positions[0]  # Assume the first position is the current one
            return current_position.get("companyName", "")
        return ""
    
    def _extract_skills(self, person):
        """Extract skills from a person's profile"""
        skills = person.get("skills", {}).get("elements", [])
        return [skill.get("name", "") for skill in skills]
    
    def _get_dummy_data(self, keywords=None, title=None, company=None, location=None):
        """Generate dummy data that reflects the search parameters"""
        print("Generating dummy data based on search parameters")
        
        # Base dummy profiles
        dummy_profiles = [
            {
                'id': 'linkedin-12345',
                'name': 'John Doe',
                'current_title': 'CTO',
                'current_company': 'Tech Corp',
                'location': 'San Francisco, CA',
                'industry': 'Technology',
                'linkedin_url': 'https://linkedin.com/in/johndoe',
                'skills': ['Leadership', 'Software Development', 'Cloud Computing', 'AI/ML'],
            },
            {
                'id': 'linkedin-67890',
                'name': 'Jane Smith',
                'current_title': 'VP of Engineering',
                'current_company': 'Software Inc',
                'location': 'New York, NY',
                'industry': 'Technology',
                'linkedin_url': 'https://linkedin.com/in/janesmith',
                'skills': ['Engineering Management', 'Product Development', 'Team Leadership'],
            },
            {
                'id': 'linkedin-54321',
                'name': 'Bob Johnson',
                'current_title': 'Senior Developer',
                'current_company': 'Dev Solutions',
                'location': 'Austin, TX',
                'industry': 'Technology',
                'linkedin_url': 'https://linkedin.com/in/bobjohnson',
                'skills': ['JavaScript', 'React', 'Node.js', 'Full Stack Development'],
            }
        ]
        
        # Create additional dynamic profiles based on search parameters
        if location or title or company:
            # Generate a few dummy names
            first_names = ['Alex', 'Sarah', 'Michael', 'Emily', 'David', 'Jennifer', 'James', 'Lisa']
            last_names = ['Williams', 'Brown', 'Jones', 'Miller', 'Davis', 'Garcia', 'Taylor', 'Thomas']
            
            # Generate profiles that match the search parameters
            for i in range(3):  # Generate 3 additional profiles
                random_id = f'linkedin-{random.randint(10000, 99999)}'
                random_first = random.choice(first_names)
                random_last = random.choice(last_names)
                
                # Use the provided title or a generic one
                profile_title = title if title else random.choice([
                    'Software Engineer', 'Product Manager', 'Marketing Director', 
                    'Sales Representative', 'Data Scientist', 'UX Designer'
                ])
                
                # Use the provided company or a generic one
                profile_company = company if company else random.choice([
                    'Google', 'Microsoft', 'Amazon', 'Apple', 'Facebook', 
                    'Netflix', 'Adobe', 'Salesforce', 'Oracle'
                ])
                
                # Use the provided location or a generic one
                profile_location = location if location else random.choice([
                    'San Francisco, CA', 'New York, NY', 'Seattle, WA', 
                    'Austin, TX', 'Boston, MA', 'Chicago, IL', 'Los Angeles, CA'
                ])
                
                # Generate profile
                profile = {
                    'id': random_id,
                    'name': f'{random_first} {random_last}',
                    'current_title': profile_title,
                    'current_company': profile_company,
                    'location': profile_location,
                    'industry': 'Technology',
                    'linkedin_url': f'https://linkedin.com/in/{random_first.lower()}{random_last.lower()}',
                    'skills': ['Leadership', 'Management', 'Communication', 'Strategy'],
                }
                
                dummy_profiles.append(profile)
        
        # Filter results based on search parameters
        filtered_profiles = dummy_profiles
        
        if title:
            filtered_profiles = [p for p in filtered_profiles if title.lower() in p['current_title'].lower()]
            
        if company:
            filtered_profiles = [p for p in filtered_profiles if company.lower() in p['current_company'].lower()]
            
        if location:
            filtered_profiles = [p for p in filtered_profiles if location.lower() in p['location'].lower()]
            
        if keywords:
            filtered_profiles = [p for p in filtered_profiles if 
                                keywords.lower() in p['name'].lower() or 
                                keywords.lower() in p['current_title'].lower() or
                                keywords.lower() in p['current_company'].lower() or
                                any(keywords.lower() in skill.lower() for skill in p['skills'])]
        
        # Ensure we return at least the base set if no matches
        return filtered_profiles if filtered_profiles else dummy_profiles
    
    def get_profile(self, username):
        """
        Get LinkedIn profile by username
        
        Args:
            username (str): LinkedIn username
            
        Returns:
            dict: LinkedIn profile data
        """
        # In a real implementation, this would call the LinkedIn API
        # For now, we'll return dummy data
        
        print(f"Getting LinkedIn profile for username: {username}")
        
        # Return dummy data
        return {
            'id': 'linkedin-12345',
            'name': 'John Doe',
            'current_title': 'CTO',
            'current_company': 'Tech Corp',
            'location': 'San Francisco, CA',
            'industry': 'Technology',
            'linkedin_url': f'https://linkedin.com/in/{username}',
            'skills': ['Leadership', 'Software Development', 'Cloud Computing', 'AI/ML'],
            'experience': [
                {
                    'title': 'CTO',
                    'company': 'Tech Corp',
                    'start_date': '2020-01',
                    'end_date': None,
                    'current': True
                },
                {
                    'title': 'VP of Engineering',
                    'company': 'Previous Corp',
                    'start_date': '2015-03',
                    'end_date': '2019-12',
                    'current': False
                }
            ],
            'education': [
                {
                    'school': 'Stanford University',
                    'degree': 'Master of Science',
                    'field': 'Computer Science',
                    'start_date': '2010',
                    'end_date': '2012'
                }
            ],
            'source': 'linkedin'
        }
    
    def get_company(self, company_name):
        """
        Get LinkedIn company by name
        
        Args:
            company_name (str): Company name
            
        Returns:
            dict: LinkedIn company data
        """
        # In a real implementation, this would call the LinkedIn API
        # For now, we'll return dummy data
        
        print(f"Getting LinkedIn company data for: {company_name}")
        
        # Return dummy data
        return {
            'id': 'linkedin-company-12345',
            'name': company_name,
            'industry': 'Technology',
            'size': '51-200 employees',
            'location': 'San Francisco, CA',
            'website': f'https://{company_name.lower().replace(" ", "")}.com',
            'linkedin_url': f'https://linkedin.com/company/{company_name.lower().replace(" ", "")}',
            'description': f'{company_name} is a leading technology company specializing in innovative solutions.',
            'founded': '2015',
            'specialties': ['Software Development', 'Cloud Computing', 'AI/ML'],
            'source': 'linkedin'
        }


class TwitterConnector:
    """Class for connecting to Twitter API"""
    
    def __init__(self, config):
        """
        Initialize the Twitter connector
        
        Args:
            config (Config): Configuration object with API settings
        """
        self.api_key = config.get_api_settings().get('twitter_api_key')
    
    def search_users(self, query, count=20):
        """
        Search for users on Twitter
        
        Args:
            query (str): Search query
            count (int): Number of results to return
            
        Returns:
            list: List of users matching the search criteria
        """
        # In a real implementation, this would call the Twitter API
        # For now, we'll return dummy data
        
        print(f"Searching Twitter for users with query: {query}, count: {count}")
        
        # Return dummy data
        return [
            {
                'id': 'twitter-12345',
                'name': 'John Doe',
                'username': 'johndoe',
                'description': 'CTO @TechCorp | Tech enthusiast | Building the future',
                'location': 'San Francisco, CA',
                'twitter_url': 'https://twitter.com/johndoe',
                'followers_count': 5000,
                'following_count': 1000,
                'tweets_count': 3000,
                'source': 'twitter'
            },
            {
                'id': 'twitter-67890',
                'name': 'Jane Smith',
                'username': 'janesmith',
                'description': 'VP of Engineering @SoftwareInc | Software architect | Tech speaker',
                'location': 'New York, NY',
                'twitter_url': 'https://twitter.com/janesmith',
                'followers_count': 3500,
                'following_count': 800,
                'tweets_count': 2000,
                'source': 'twitter'
            }
        ]
    
    def get_user(self, username):
        """
        Get Twitter user by username
        
        Args:
            username (str): Twitter username
            
        Returns:
            dict: Twitter user data
        """
        # In a real implementation, this would call the Twitter API
        # For now, we'll return dummy data
        
        print(f"Getting Twitter user data for username: {username}")
        
        # Return dummy data
        return {
            'id': 'twitter-12345',
            'name': 'John Doe',
            'username': username,
            'description': 'CTO @TechCorp | Tech enthusiast | Building the future',
            'location': 'San Francisco, CA',
            'twitter_url': f'https://twitter.com/{username}',
            'followers_count': 5000,
            'following_count': 1000,
            'tweets_count': 3000,
            'source': 'twitter'
        }
    
    def get_tweets(self, username, count=20):
        """
        Get tweets for a user
        
        Args:
            username (str): Twitter username
            count (int): Number of tweets to return
            
        Returns:
            list: List of tweets
        """
        # In a real implementation, this would call the Twitter API
        # For now, we'll return dummy data
        
        print(f"Getting tweets for username: {username}, count: {count}")
        
        # Return dummy data
        return [
            {
                'id': 'tweet-12345',
                'text': 'Excited about our new AI product launch! #TechCorp #Innovation',
                'created_at': 'Mon Mar 13 2025 10:30:00 GMT+0000',
                'retweet_count': 50,
                'favorite_count': 150
            },
            {
                'id': 'tweet-67890',
                'text': 'Looking to hire senior engineers for our growing team. DM if interested! #Hiring #TechJobs',
                'created_at': 'Sun Mar 12 2025 15:45:00 GMT+0000',
                'retweet_count': 30,
                'favorite_count': 80
            },
            {
                'id': 'tweet-54321',
                'text': 'Just published a new blog post on our tech stack. Check it out! https://techcorp.com/blog/tech-stack',
                'created_at': 'Fri Mar 10 2025 09:15:00 GMT+0000',
                'retweet_count': 25,
                'favorite_count': 95
            }
        ]
