import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

const ResultsPage = () => {
  const [leads, setLeads] = useState([]);
  const [filteredLeads, setFilteredLeads] = useState([]);
  const [loading, setLoading] = useState(false);
  const [exportLoading, setExportLoading] = useState(false);
  const [exportLink, setExportLink] = useState('');
  const [selectedLeads, setSelectedLeads] = useState([]);
  const [filters, setFilters] = useState({
    minScore: 0,
    industry: '',
    location: ''
  });

  useEffect(() => {
    // Load leads from localStorage
    const savedLeads = localStorage.getItem('leadResults');
    if (savedLeads) {
      const parsedLeads = JSON.parse(savedLeads);
      setLeads(parsedLeads);
      setFilteredLeads(parsedLeads);
      
      // Initialize selected leads (select all by default)
      setSelectedLeads(parsedLeads.map(lead => lead.id));
    }
  }, []);

  useEffect(() => {
    // Apply filters whenever filters change
    if (leads.length > 0) {
      let results = [...leads];
      
      if (filters.minScore > 0) {
        results = results.filter(lead => lead.score >= filters.minScore);
      }
      
      if (filters.industry) {
        results = results.filter(lead => 
          lead.industry && lead.industry.toLowerCase().includes(filters.industry.toLowerCase())
        );
      }
      
      if (filters.location) {
        results = results.filter(lead => 
          lead.location && lead.location.toLowerCase().includes(filters.location.toLowerCase())
        );
      }
      
      setFilteredLeads(results);
    }
  }, [filters, leads]);

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters({
      ...filters,
      [name]: value
    });
  };

  const toggleLeadSelection = (leadId) => {
    if (selectedLeads.includes(leadId)) {
      setSelectedLeads(selectedLeads.filter(id => id !== leadId));
    } else {
      setSelectedLeads([...selectedLeads, leadId]);
    }
  };

  const handleSelectAll = (e) => {
    if (e.target.checked) {
      setSelectedLeads(filteredLeads.map(lead => lead.id));
    } else {
      setSelectedLeads([]);
    }
  };

  const exportToExcel = async () => {
    if (selectedLeads.length === 0) {
      alert('Please select at least one lead to export');
      return;
    }
    
    setExportLoading(true);
    
    try {
      const leadsToExport = leads.filter(lead => selectedLeads.includes(lead.id));
      
      const response = await axios.post('/api/export', {
        leads: leadsToExport
      });
      
      if (response.data && response.data.filename) {
        setExportLink(`/api/download/${response.data.filename}`);
      }
    } catch (error) {
      console.error('Error exporting leads:', error);
      alert('There was an error exporting leads. Please try again.');
    } finally {
      setExportLoading(false);
    }
  };

  const getScoreClass = (score) => {
    if (score >= 80) return 'high-score';
    if (score >= 60) return 'medium-score';
    return 'low-score';
  };

  return (
    <div className="results-page">
      <div className="results-header d-flex justify-content-between align-items-center mb-4">
        <h2>Lead Results</h2>
        <div>
          <Link to="/" className="btn btn-outline-primary me-2">
            <i className="fas fa-search me-1"></i> New Search
          </Link>
          {exportLink ? (
            <a 
              href={exportLink} 
              className="btn btn-success"
              download
            >
              <i className="fas fa-download me-1"></i> Download Excel
            </a>
          ) : (
            <button 
              className="btn btn-primary" 
              onClick={exportToExcel}
              disabled={exportLoading || selectedLeads.length === 0}
            >
              {exportLoading ? (
                <>
                  <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                  Exporting...
                </>
              ) : (
                <>
                  <i className="fas fa-file-excel me-1"></i> Export to Excel
                </>
              )}
            </button>
          )}
        </div>
      </div>
      
      <div className="filter-section mb-4">
        <div className="row">
          <div className="col-md-3">
            <label htmlFor="minScore" className="form-label">Minimum Score</label>
            <input
              type="range"
              className="form-range"
              id="minScore"
              name="minScore"
              min="0"
              max="100"
              value={filters.minScore}
              onChange={handleFilterChange}
            />
            <div className="d-flex justify-content-between">
              <small>0</small>
              <small>{filters.minScore}</small>
              <small>100</small>
            </div>
          </div>
          
          <div className="col-md-4">
            <label htmlFor="industry" className="form-label">Industry</label>
            <input
              type="text"
              className="form-control"
              id="industry"
              name="industry"
              value={filters.industry}
              onChange={handleFilterChange}
              placeholder="Filter by industry"
            />
          </div>
          
          <div className="col-md-4">
            <label htmlFor="location" className="form-label">Location</label>
            <input
              type="text"
              className="form-control"
              id="location"
              name="location"
              value={filters.location}
              onChange={handleFilterChange}
              placeholder="Filter by location"
            />
          </div>
        </div>
      </div>
      
      <div className="results-container">
        {filteredLeads.length === 0 ? (
          <div className="alert alert-info">
            No leads found. Try adjusting your filters or performing a new search.
          </div>
        ) : (
          <>
            <div className="table-responsive">
              <table className="table table-hover">
                <thead>
                  <tr>
                    <th>
                      <input 
                        type="checkbox" 
                        className="form-check-input" 
                        checked={selectedLeads.length === filteredLeads.length && filteredLeads.length > 0}
                        onChange={handleSelectAll}
                      />
                    </th>
                    <th>Name</th>
                    <th>Title</th>
                    <th>Company</th>
                    <th>Location</th>
                    <th>Industry</th>
                    <th>Score</th>
                    <th>Profile</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredLeads.map(lead => (
                    <tr key={lead.id}>
                      <td>
                        <input 
                          type="checkbox" 
                          className="form-check-input" 
                          checked={selectedLeads.includes(lead.id)}
                          onChange={() => toggleLeadSelection(lead.id)}
                        />
                      </td>
                      <td>{lead.name}</td>
                      <td>{lead.current_title}</td>
                      <td>{lead.current_company}</td>
                      <td>{lead.location}</td>
                      <td>{lead.industry}</td>
                      <td>
                        <span className={`score-badge ${getScoreClass(lead.score)}`}>
                          {lead.score}
                        </span>
                      </td>
                      <td>
                        {lead.linkedin_url && (
                          <a href={lead.linkedin_url} target="_blank" rel="noopener noreferrer" className="social-icon">
                            <i className="fab fa-linkedin"></i>
                          </a>
                        )}
                        
                        {lead.twitter_url && (
                          <a href={lead.twitter_url} target="_blank" rel="noopener noreferrer" className="social-icon twitter-icon">
                            <i className="fab fa-twitter"></i>
                          </a>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            
            <div className="results-summary mt-3">
              <p>Showing {filteredLeads.length} leads out of {leads.length} total leads</p>
              <p>{selectedLeads.length} leads selected for export</p>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default ResultsPage; 