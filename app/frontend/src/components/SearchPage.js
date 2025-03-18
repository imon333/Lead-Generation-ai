import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const SearchPage = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    query: '',
    title: '',
    company: '',
    location: '',
    sources: ['linkedin']
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSourceChange = (source) => {
    const currentSources = [...formData.sources];
    
    if (currentSources.includes(source)) {
      // Remove the source if it's already selected
      setFormData({
        ...formData,
        sources: currentSources.filter(s => s !== source)
      });
    } else {
      // Add the source if it's not selected
      setFormData({
        ...formData,
        sources: [...currentSources, source]
      });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const response = await axios.post('/api/search', formData);
      
      if (response.data && response.data.leads) {
        // Store leads in localStorage for the results page
        localStorage.setItem('leadResults', JSON.stringify(response.data.leads));
        
        // Navigate to results page
        navigate('/results');
      }
    } catch (error) {
      console.error('Error searching for leads:', error);
      alert('There was an error searching for leads. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="search-page">
      <div className="search-container">
        <h2 className="mb-4">Find Your Ideal Leads</h2>
        
        <form onSubmit={handleSubmit}>
          <div className="row mb-4">
            <div className="col-md-12 mb-3">
              <label htmlFor="query" className="form-label">Search Keywords</label>
              <input
                type="text"
                className="form-control"
                id="query"
                name="query"
                value={formData.query}
                onChange={handleChange}
                placeholder="E.g., Sales Manager, Marketing Director"
              />
              <small className="text-muted">Enter keywords to search for in profiles</small>
            </div>
          </div>
          
          <div className="row mb-4">
            <div className="col-md-4 mb-3">
              <label htmlFor="title" className="form-label">Job Title</label>
              <input
                type="text"
                className="form-control"
                id="title"
                name="title"
                value={formData.title}
                onChange={handleChange}
                placeholder="E.g., CTO, Marketing Director"
              />
            </div>
            
            <div className="col-md-4 mb-3">
              <label htmlFor="company" className="form-label">Company</label>
              <input
                type="text"
                className="form-control"
                id="company"
                name="company"
                value={formData.company}
                onChange={handleChange}
                placeholder="E.g., Acme Inc., Tech Startups"
              />
            </div>
            
            <div className="col-md-4 mb-3">
              <label htmlFor="location" className="form-label">Location</label>
              <input
                type="text"
                className="form-control"
                id="location"
                name="location"
                value={formData.location}
                onChange={handleChange}
                placeholder="E.g., San Francisco, London"
              />
            </div>
          </div>
          
          <div className="row mb-4">
            <div className="col-12">
              <label className="form-label">Data Sources</label>
              <div className="d-flex">
                <div className="form-check me-4">
                  <input
                    className="form-check-input"
                    type="checkbox"
                    id="linkedinSource"
                    checked={formData.sources.includes('linkedin')}
                    onChange={() => handleSourceChange('linkedin')}
                  />
                  <label className="form-check-label" htmlFor="linkedinSource">
                    <i className="fab fa-linkedin text-primary me-1"></i> LinkedIn
                  </label>
                </div>
                
                <div className="form-check me-4">
                  <input
                    className="form-check-input"
                    type="checkbox"
                    id="twitterSource"
                    checked={formData.sources.includes('twitter')}
                    onChange={() => handleSourceChange('twitter')}
                  />
                  <label className="form-check-label" htmlFor="twitterSource">
                    <i className="fab fa-twitter text-info me-1"></i> Twitter
                  </label>
                </div>
              </div>
            </div>
          </div>
          
          <div className="d-grid gap-2 d-md-flex justify-content-md-end">
            <button 
              type="submit" 
              className="btn btn-primary btn-lg px-4"
              disabled={loading}
            >
              {loading ? (
                <>
                  <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                  Searching...
                </>
              ) : (
                <>
                  <i className="fas fa-search me-2"></i> Find Leads
                </>
              )}
            </button>
          </div>
        </form>
      </div>
      
      <div className="info-container mt-4 p-4 bg-light rounded">
        <h3>How it works</h3>
        <div className="row mt-3">
          <div className="col-md-4 mb-3">
            <div className="card h-100">
              <div className="card-body">
                <h5 className="card-title">1. Define your criteria</h5>
                <p className="card-text">Enter job titles, companies, locations, and keywords to find your ideal prospects.</p>
              </div>
            </div>
          </div>
          
          <div className="col-md-4 mb-3">
            <div className="card h-100">
              <div className="card-body">
                <h5 className="card-title">2. Get qualified leads</h5>
                <p className="card-text">Our AI analyzes profiles and ranks them based on your criteria and likelihood to convert.</p>
              </div>
            </div>
          </div>
          
          <div className="col-md-4 mb-3">
            <div className="card h-100">
              <div className="card-body">
                <h5 className="card-title">3. Export and reach out</h5>
                <p className="card-text">Download your leads in Excel format and start your outreach campaigns.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SearchPage; 