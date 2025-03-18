# Lead Generation Agent - Usage Instructions

This document provides instructions on how to use the Lead Generation Agent in Google Colab.

## Overview

The Lead Generation Agent is a Python-based tool that helps you find, analyze, and score potential leads for your business. It uses data from LinkedIn and Twitter to identify promising leads, score them based on various factors, and provide actionable suggestions.

## Setup Instructions

### 1. Upload the Project to Google Colab

1. Go to [Google Colab](https://colab.research.google.com/)
2. Click on "File" > "Upload notebook"
3. Upload the `lead_generation_agent.ipynb` file from the `notebooks` folder

### 2. Upload the Project Files

1. In Google Colab, click on the folder icon in the left sidebar to open the file browser
2. Create the following folder structure:
   - `src`
   - `data`
3. Upload the Python files from the `src` folder to the `src` folder in Colab
4. Upload the Python files from the `data` folder to the `data` folder in Colab

### 3. Run the Notebook

1. Open the uploaded `lead_generation_agent.ipynb` notebook
2. Run the cells in order by clicking the play button next to each cell or by pressing Shift+Enter

## Using the Lead Generation Agent

The notebook is organized into sections that demonstrate different features of the Lead Generation Agent:

### 1. Setup and Initialization

The first few cells set up the environment and initialize the Lead Generation Agent. Run these cells to install required packages and import necessary modules.

### 2. Searching for Leads

Use the search functionality to find potential leads based on criteria like:
- Keywords
- Job titles
- Companies
- Locations

Example:
```python
search_results = agent.search(
    query="technology leadership",
    title="CTO",
    company="Tech",
    location="San Francisco"
)
```

### 3. Analyzing Lead Data

The notebook includes cells for analyzing lead data, including:
- Displaying lead information in tables
- Visualizing lead distribution by score
- Analyzing leads by industry and title level

### 4. Scoring and Ranking Leads

The Lead Generation Agent scores leads based on factors like:
- Decision-maker status
- Company fit
- Growth potential
- Skill relevance
- Location relevance
- Engagement potential

You can view score components for individual leads and compare leads based on their scores.

### 5. Generating Lead Suggestions

Generate actionable lead suggestions with:
```python
suggestions = agent.generate_suggestions(
    industries=['Technology'],
    title_levels=['C-Level', 'VP/Director'],
    min_score=70
)
```

Each suggestion includes:
- Lead information
- A descriptive title
- A detailed description
- A recommended action
- The suggestion type (hot, warm, or cold)

### 6. Analyzing Industry and Skill Trends

The notebook includes cells for analyzing industry and skill trends, which can help you identify promising areas for lead generation.

## Customizing the Lead Generation Agent

### Modifying Scoring Settings

You can customize how leads are scored by modifying the scoring settings:

```python
config.update_scoring_settings({
    'decision_maker_weight': 0.30,  # Increase weight for decision makers
    'company_fit_weight': 0.25,
    'growth_potential_weight': 0.15,
    'skill_relevance_weight': 0.10,
    'location_relevance_weight': 0.10,
    'engagement_potential_weight': 0.10
})
```

### Adding Your Own Data

You can add your own lead data to the agent:

```python
my_lead = {
    'id': 'custom-12345',
    'name': 'Your Lead Name',
    'current_title': 'CEO',
    'current_company': 'Your Company',
    'location': 'Your Location',
    'industry': 'Your Industry',
    'skills': ['Skill 1', 'Skill 2', 'Skill 3']
}

agent.add_lead(my_lead)
```

### Exporting Data

You can export lead data to CSV or JSON:

```python
# Initialize storage manager
storage_manager = StorageManager()

# Add leads to storage
for lead in all_leads:
    storage_manager.save_lead(lead)

# Export to CSV
csv_path = storage_manager.export_to_csv('leads')
print(f"Leads exported to: {csv_path}")

# Export to JSON
json_path = storage_manager.export_to_json('leads')
print(f"Leads exported to: {json_path}")
```

## Troubleshooting

### Common Issues

1. **ImportError**: Make sure all the required files are uploaded to the correct folders in Google Colab.
2. **ModuleNotFoundError**: Run the cell that installs the required packages.
3. **AttributeError**: Make sure you're using the correct method names and parameters.

### Getting Help

If you encounter any issues, check the documentation in the code comments or refer to the example code in the notebook.

## Next Steps

Once you're comfortable with the basic functionality, you can:

1. Connect to real APIs by updating the API connectors
2. Add more data sources
3. Customize the scoring algorithm for your specific needs
4. Implement a database for persistent storage
5. Create a web interface for easier interaction

## License

This project is provided for educational purposes. Use responsibly and in accordance with the terms of service of any APIs you connect to.
