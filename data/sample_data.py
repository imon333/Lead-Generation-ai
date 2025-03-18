"""
Sample data for the Lead Generation Agent
"""

# Sample leads data
SAMPLE_LEADS = [
    {
        'id': '12345',
        'name': 'John Doe',
        'current_title': 'CTO',
        'current_company': 'Tech Corp',
        'location': 'San Francisco, CA',
        'industry': 'Technology',
        'linkedin_url': 'https://linkedin.com/in/johndoe',
        'twitter_url': 'https://twitter.com/johndoe',
        'score': 85,
        'score_components': {
            'decision_maker': 1.0,
            'company_fit': 0.8,
            'growth_potential': 0.7,
            'skill_relevance': 0.9,
            'location_relevance': 1.0,
            'engagement_potential': 0.7
        },
        'skills': ['Leadership', 'Software Development', 'Cloud Computing', 'AI/ML'],
        'engagement_signals': ['active_poster', 'job_change_6mo', 'growing_company']
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
        'score': 78,
        'score_components': {
            'decision_maker': 0.8,
            'company_fit': 0.8,
            'growth_potential': 0.6,
            'skill_relevance': 0.7,
            'location_relevance': 1.0,
            'engagement_potential': 0.6
        },
        'skills': ['Software Architecture', 'Team Leadership', 'Agile Methodologies'],
        'engagement_signals': ['active_poster']
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
        'score': 65,
        'score_components': {
            'decision_maker': 0.4,
            'company_fit': 0.7,
            'growth_potential': 0.8,
            'skill_relevance': 0.9,
            'location_relevance': 0.5,
            'engagement_potential': 0.4
        },
        'skills': ['JavaScript', 'React', 'Node.js'],
        'engagement_signals': []
    },
    {
        'id': '13579',
        'name': 'Sarah Williams',
        'current_title': 'CEO',
        'current_company': 'Startup Innovations',
        'location': 'Boston, MA',
        'industry': 'Healthcare',
        'linkedin_url': 'https://linkedin.com/in/sarahwilliams',
        'twitter_url': 'https://twitter.com/sarahwilliams',
        'score': 82,
        'score_components': {
            'decision_maker': 1.0,
            'company_fit': 0.6,
            'growth_potential': 0.9,
            'skill_relevance': 0.7,
            'location_relevance': 0.8,
            'engagement_potential': 0.9
        },
        'skills': ['Leadership', 'Entrepreneurship', 'Healthcare IT'],
        'engagement_signals': ['active_poster', 'growing_company', 'recent_funding']
    },
    {
        'id': '24680',
        'name': 'Michael Chen',
        'current_title': 'Director of Product',
        'current_company': 'Global Solutions',
        'location': 'Seattle, WA',
        'industry': 'E-commerce',
        'linkedin_url': 'https://linkedin.com/in/michaelchen',
        'twitter_url': 'https://twitter.com/michaelchen',
        'score': 75,
        'score_components': {
            'decision_maker': 0.8,
            'company_fit': 0.7,
            'growth_potential': 0.7,
            'skill_relevance': 0.8,
            'location_relevance': 0.7,
            'engagement_potential': 0.8
        },
        'skills': ['Product Management', 'UX Design', 'E-commerce'],
        'engagement_signals': ['active_poster', 'job_change_6mo']
    },
    {
        'id': '97531',
        'name': 'Emily Davis',
        'current_title': 'Marketing Manager',
        'current_company': 'Brand Builders',
        'location': 'Chicago, IL',
        'industry': 'Marketing',
        'linkedin_url': 'https://linkedin.com/in/emilydavis',
        'twitter_url': 'https://twitter.com/emilydavis',
        'score': 62,
        'score_components': {
            'decision_maker': 0.6,
            'company_fit': 0.5,
            'growth_potential': 0.6,
            'skill_relevance': 0.7,
            'location_relevance': 0.7,
            'engagement_potential': 0.6
        },
        'skills': ['Digital Marketing', 'Social Media', 'Content Strategy'],
        'engagement_signals': ['active_poster']
    },
    {
        'id': '86420',
        'name': 'David Wilson',
        'current_title': 'CFO',
        'current_company': 'Finance Solutions',
        'location': 'Miami, FL',
        'industry': 'Finance',
        'linkedin_url': 'https://linkedin.com/in/davidwilson',
        'twitter_url': 'https://twitter.com/davidwilson',
        'score': 79,
        'score_components': {
            'decision_maker': 1.0,
            'company_fit': 0.6,
            'growth_potential': 0.7,
            'skill_relevance': 0.6,
            'location_relevance': 0.9,
            'engagement_potential': 0.7
        },
        'skills': ['Financial Analysis', 'Investment', 'Strategic Planning'],
        'engagement_signals': ['job_change_6mo', 'growing_company']
    },
    {
        'id': '11223',
        'name': 'Jennifer Lopez',
        'current_title': 'Head of Sales',
        'current_company': 'Growth Enterprises',
        'location': 'Los Angeles, CA',
        'industry': 'Sales',
        'linkedin_url': 'https://linkedin.com/in/jenniferlopez',
        'twitter_url': 'https://twitter.com/jenniferlopez',
        'score': 72,
        'score_components': {
            'decision_maker': 0.7,
            'company_fit': 0.7,
            'growth_potential': 0.8,
            'skill_relevance': 0.6,
            'location_relevance': 0.8,
            'engagement_potential': 0.7
        },
        'skills': ['Sales Strategy', 'Negotiation', 'Client Relationship'],
        'engagement_signals': ['active_poster', 'growing_company']
    },
    {
        'id': '33445',
        'name': 'Robert Brown',
        'current_title': 'CIO',
        'current_company': 'Tech Innovations',
        'location': 'Denver, CO',
        'industry': 'Technology',
        'linkedin_url': 'https://linkedin.com/in/robertbrown',
        'twitter_url': 'https://twitter.com/robertbrown',
        'score': 84,
        'score_components': {
            'decision_maker': 1.0,
            'company_fit': 0.8,
            'growth_potential': 0.7,
            'skill_relevance': 0.9,
            'location_relevance': 0.7,
            'engagement_potential': 0.8
        },
        'skills': ['IT Strategy', 'Digital Transformation', 'Cloud Computing'],
        'engagement_signals': ['active_poster', 'growing_company', 'recent_funding']
    },
    {
        'id': '55667',
        'name': 'Lisa Taylor',
        'current_title': 'VP of Marketing',
        'current_company': 'Digital Brands',
        'location': 'Atlanta, GA',
        'industry': 'Marketing',
        'linkedin_url': 'https://linkedin.com/in/lisataylor',
        'twitter_url': 'https://twitter.com/lisataylor',
        'score': 76,
        'score_components': {
            'decision_maker': 0.8,
            'company_fit': 0.7,
            'growth_potential': 0.7,
            'skill_relevance': 0.8,
            'location_relevance': 0.7,
            'engagement_potential': 0.8
        },
        'skills': ['Brand Strategy', 'Digital Marketing', 'Market Research'],
        'engagement_signals': ['active_poster', 'job_change_6mo']
    }
]

# Sample companies data
SAMPLE_COMPANIES = [
    {
        'id': '12345',
        'name': 'Tech Corp',
        'industry': 'Technology',
        'size': '51-200 employees',
        'location': 'San Francisco, CA',
        'website': 'https://techcorp.com',
        'linkedin_url': 'https://linkedin.com/company/techcorp',
        'description': 'Innovative tech company',
        'founded': '2015',
        'previous_size': '11-50 employees',
        'previous_size_date': '2020-01',
        'job_postings': 15,
        'recent_hires': 8
    },
    {
        'id': '67890',
        'name': 'Software Inc',
        'industry': 'Technology',
        'size': '201-500 employees',
        'location': 'New York, NY',
        'website': 'https://softwareinc.com',
        'linkedin_url': 'https://linkedin.com/company/softwareinc',
        'description': 'Enterprise software solutions',
        'founded': '2010',
        'previous_size': '51-200 employees',
        'previous_size_date': '2018-06',
        'job_postings': 25,
        'recent_hires': 12
    },
    {
        'id': '54321',
        'name': 'Dev Solutions',
        'industry': 'Technology',
        'size': '11-50 employees',
        'location': 'Austin, TX',
        'website': 'https://devsolutions.com',
        'linkedin_url': 'https://linkedin.com/company/devsolutions',
        'description': 'Custom software development',
        'founded': '2018',
        'previous_size': '1-10 employees',
        'previous_size_date': '2019-03',
        'job_postings': 5,
        'recent_hires': 3
    },
    {
        'id': '13579',
        'name': 'Startup Innovations',
        'industry': 'Healthcare',
        'size': '11-50 employees',
        'location': 'Boston, MA',
        'website': 'https://startupinnovations.com',
        'linkedin_url': 'https://linkedin.com/company/startupinnovations',
        'description': 'Healthcare technology solutions',
        'founded': '2019',
        'previous_size': '1-10 employees',
        'previous_size_date': '2020-01',
        'job_postings': 8,
        'recent_hires': 5
    },
    {
        'id': '24680',
        'name': 'Global Solutions',
        'industry': 'E-commerce',
        'size': '501-1000 employees',
        'location': 'Seattle, WA',
        'website': 'https://globalsolutions.com',
        'linkedin_url': 'https://linkedin.com/company/globalsolutions',
        'description': 'Global e-commerce platform',
        'founded': '2008',
        'previous_size': '201-500 employees',
        'previous_size_date': '2017-09',
        'job_postings': 30,
        'recent_hires': 15
    }
]

# Sample skills data
SAMPLE_SKILLS_DATA = [
    {'name': 'AI/ML', 'frequency': 120, 'growth_rate': 0.25},
    {'name': 'Cloud Computing', 'frequency': 150, 'growth_rate': 0.15},
    {'name': 'DevOps', 'frequency': 100, 'growth_rate': 0.10},
    {'name': 'Blockchain', 'frequency': 50, 'growth_rate': 0.30},
    {'name': 'Data Science', 'frequency': 130, 'growth_rate': 0.20},
    {'name': 'React', 'frequency': 140, 'growth_rate': 0.05},
    {'name': 'Python', 'frequency': 160, 'growth_rate': 0.10},
    {'name': 'JavaScript', 'frequency': 170, 'growth_rate': 0.00},
    {'name': 'Cybersecurity', 'frequency': 90, 'growth_rate': 0.18},
    {'name': 'UX Design', 'frequency': 80, 'growth_rate': 0.08}
]

# Sample industry data
SAMPLE_INDUSTRY_DATA = [
    {'name': 'Technology', 'companies': 50, 'growth_rate': 0.20},
    {'name': 'Healthcare', 'companies': 30, 'growth_rate': 0.15},
    {'name': 'Finance', 'companies': 40, 'growth_rate': 0.10},
    {'name': 'E-commerce', 'companies': 25, 'growth_rate': 0.25},
    {'name': 'Marketing', 'companies': 20, 'growth_rate': 0.05},
    {'name': 'Manufacturing', 'companies': 35, 'growth_rate': -0.02},
    {'name': 'Retail', 'companies': 30, 'growth_rate': -0.05},
    {'name': 'Education', 'companies': 15, 'growth_rate': 0.08},
    {'name': 'Real Estate', 'companies': 20, 'growth_rate': 0.03},
    {'name': 'Entertainment', 'companies': 10, 'growth_rate': 0.12}
]
