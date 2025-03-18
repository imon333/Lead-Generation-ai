"""
Visualization utilities for the Lead Generation Agent
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from IPython.display import display

class LeadVisualizer:
    """Class for visualizing lead data"""
    
    def __init__(self, figsize=(10, 6)):
        """
        Initialize the LeadVisualizer
        
        Args:
            figsize (tuple): Default figure size for plots
        """
        self.figsize = figsize
        # Set the style for all visualizations
        sns.set(style="whitegrid")
    
    def plot_lead_distribution_by_score(self, leads):
        """
        Plot distribution of leads by score
        
        Args:
            leads (list): List of lead dictionaries with scores
            
        Returns:
            matplotlib.figure.Figure: The created figure
        """
        # Extract scores
        scores = [lead.get('score', 0) for lead in leads]
        
        # Create figure
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Create histogram
        sns.histplot(scores, bins=10, kde=True, ax=ax)
        
        # Add labels and title
        ax.set_xlabel('Lead Score')
        ax.set_ylabel('Count')
        ax.set_title('Distribution of Leads by Score')
        
        # Add vertical lines for score categories
        ax.axvline(x=80, color='r', linestyle='--', label='Hot Lead Threshold')
        ax.axvline(x=60, color='orange', linestyle='--', label='Warm Lead Threshold')
        
        # Add legend
        ax.legend()
        
        return fig
    
    def plot_leads_by_industry(self, leads):
        """
        Plot leads by industry
        
        Args:
            leads (list): List of lead dictionaries with industry
            
        Returns:
            matplotlib.figure.Figure: The created figure
        """
        # Count leads by industry
        industry_counts = {}
        for lead in leads:
            industry = lead.get('industry', 'Unknown')
            industry_counts[industry] = industry_counts.get(industry, 0) + 1
        
        # Sort by count
        sorted_industries = sorted(industry_counts.items(), key=lambda x: x[1], reverse=True)
        
        # Extract data for plotting
        industries = [item[0] for item in sorted_industries]
        counts = [item[1] for item in sorted_industries]
        
        # Create figure
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Create bar chart
        sns.barplot(x=counts, y=industries, ax=ax)
        
        # Add labels and title
        ax.set_xlabel('Number of Leads')
        ax.set_ylabel('Industry')
        ax.set_title('Leads by Industry')
        
        return fig
    
    def plot_leads_by_title_level(self, leads):
        """
        Plot leads by title level
        
        Args:
            leads (list): List of lead dictionaries with current_title
            
        Returns:
            matplotlib.figure.Figure: The created figure
        """
        # Categorize titles
        title_categories = {
            'C-Level': ['ceo', 'cto', 'cio', 'cfo', 'coo', 'chief'],
            'VP/Director': ['vp', 'vice president', 'director'],
            'Manager': ['manager', 'head of'],
            'Senior IC': ['senior', 'lead', 'principal'],
            'IC': []  # Default category
        }
        
        # Count leads by title category
        category_counts = {category: 0 for category in title_categories}
        
        for lead in leads:
            title = lead.get('current_title', '').lower()
            
            # Find matching category
            matched = False
            for category, keywords in title_categories.items():
                if any(keyword in title for keyword in keywords):
                    category_counts[category] += 1
                    matched = True
                    break
            
            # Default to IC if no match
            if not matched:
                category_counts['IC'] += 1
        
        # Extract data for plotting
        categories = list(category_counts.keys())
        counts = list(category_counts.values())
        
        # Create figure
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Create bar chart
        sns.barplot(x=categories, y=counts, ax=ax)
        
        # Add labels and title
        ax.set_xlabel('Title Level')
        ax.set_ylabel('Number of Leads')
        ax.set_title('Leads by Title Level')
        
        return fig
    
    def plot_score_components(self, lead):
        """
        Plot score components for a single lead
        
        Args:
            lead (dict): Lead dictionary with score_components
            
        Returns:
            matplotlib.figure.Figure: The created figure
        """
        # Extract score components
        components = lead.get('score_components', {})
        
        if not components:
            print("No score components available for this lead.")
            return None
        
        # Extract data for plotting
        categories = list(components.keys())
        scores = [components[category] for category in categories]
        
        # Create figure
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Create radar chart
        # Convert to radians
        N = len(categories)
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1]  # Close the loop
        
        # Add the first point at the end to close the polygon
        scores_for_plot = scores + [scores[0]]
        
        # Draw the polygon
        ax.plot(angles, scores_for_plot, linewidth=2, linestyle='solid')
        ax.fill(angles, scores_for_plot, alpha=0.25)
        
        # Set category labels
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)
        
        # Set y limits
        ax.set_ylim(0, 1)
        
        # Add title
        ax.set_title(f"Score Components for {lead.get('name', 'Lead')}")
        
        return fig
    
    def plot_lead_comparison(self, leads, metric='score'):
        """
        Plot comparison of leads by a specific metric
        
        Args:
            leads (list): List of lead dictionaries
            metric (str): Metric to compare (e.g., 'score', 'company_fit', etc.)
            
        Returns:
            matplotlib.figure.Figure: The created figure
        """
        # Extract data for plotting
        names = [lead.get('name', f"Lead {i}") for i, lead in enumerate(leads)]
        
        if metric == 'score':
            values = [lead.get('score', 0) for lead in leads]
            title = 'Lead Comparison by Overall Score'
            ylabel = 'Score'
        else:
            # Try to get from score_components
            values = [lead.get('score_components', {}).get(metric, 0) * 100 for lead in leads]
            title = f'Lead Comparison by {metric.replace("_", " ").title()}'
            ylabel = f'{metric.replace("_", " ").title()} Score'
        
        # Sort by value
        sorted_data = sorted(zip(names, values), key=lambda x: x[1], reverse=True)
        sorted_names = [item[0] for item in sorted_data]
        sorted_values = [item[1] for item in sorted_data]
        
        # Create figure
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Create horizontal bar chart
        sns.barplot(x=sorted_values, y=sorted_names, ax=ax)
        
        # Add labels and title
        ax.set_xlabel(ylabel)
        ax.set_ylabel('Lead')
        ax.set_title(title)
        
        return fig
    
    def display_lead_table(self, leads, columns=None):
        """
        Display leads as a formatted table
        
        Args:
            leads (list): List of lead dictionaries
            columns (list): List of columns to display
        """
        if not leads:
            print("No leads to display.")
            return
        
        # Default columns if not specified
        if columns is None:
            columns = ['name', 'current_title', 'current_company', 'location', 'score']
        
        # Create DataFrame
        df = pd.DataFrame(leads)
        
        # Select only available columns
        available_columns = [col for col in columns if col in df.columns]
        
        # Display the table
        display(df[available_columns])
    
    def plot_leads_by_location(self, leads):
        """
        Plot leads by location
        
        Args:
            leads (list): List of lead dictionaries with location
            
        Returns:
            matplotlib.figure.Figure: The created figure
        """
        # Count leads by location
        location_counts = {}
        for lead in leads:
            location = lead.get('location', 'Unknown')
            location_counts[location] = location_counts.get(location, 0) + 1
        
        # Sort by count and take top 10
        sorted_locations = sorted(location_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Extract data for plotting
        locations = [item[0] for item in sorted_locations]
        counts = [item[1] for item in sorted_locations]
        
        # Create figure
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Create bar chart
        sns.barplot(x=counts, y=locations, ax=ax)
        
        # Add labels and title
        ax.set_xlabel('Number of Leads')
        ax.set_ylabel('Location')
        ax.set_title('Top 10 Locations by Lead Count')
        
        return fig
