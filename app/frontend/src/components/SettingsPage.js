import React, { useState, useEffect } from 'react';
import axios from 'axios';

const SettingsPage = () => {
  const [settings, setSettings] = useState({
    linkedin_api_key: '',
    twitter_api_key: '',
    scoring: {
      decision_maker_weight: 0.25,
      company_fit_weight: 0.20,
      growth_potential_weight: 0.15,
      skill_relevance_weight: 0.15,
      location_relevance_weight: 0.10,
      engagement_potential_weight: 0.15
    }
  });
  
  const [loading, setLoading] = useState(false);
  const [saved, setSaved] = useState(false);
  
  useEffect(() => {
    // Fetch current settings
    const fetchSettings = async () => {
      try {
        const response = await axios.get('/api/config');
        if (response.data && response.data.scoring) {
          setSettings(prevSettings => ({
            ...prevSettings,
            scoring: response.data.scoring
          }));
        }
      } catch (error) {
        console.error('Error fetching settings:', error);
      }
    };
    
    fetchSettings();
  }, []);
  
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setSettings({
      ...settings,
      [name]: value
    });
  };
  
  const handleScoringChange = (e) => {
    const { name, value } = e.target;
    setSettings({
      ...settings,
      scoring: {
        ...settings.scoring,
        [name]: parseFloat(value)
      }
    });
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setSaved(false);
    
    try {
      await axios.post('/api/config', settings);
      setSaved(true);
      setTimeout(() => setSaved(false), 3000); // Hide the success message after 3 seconds
    } catch (error) {
      console.error('Error saving settings:', error);
      alert('There was an error saving your settings. Please try again.');
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div className="settings-page">
      <div className="settings-container search-container">
        <h2 className="mb-4">Settings</h2>
        
        {saved && (
          <div className="alert alert-success">
            Settings saved successfully!
          </div>
        )}
        
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <h4>API Keys</h4>
            <div className="row mb-3">
              <div className="col-md-6">
                <label htmlFor="linkedin_api_key" className="form-label">LinkedIn API Key</label>
                <input
                  type="password"
                  className="form-control"
                  id="linkedin_api_key"
                  name="linkedin_api_key"
                  value={settings.linkedin_api_key}
                  onChange={handleInputChange}
                  placeholder="Enter your LinkedIn API key"
                />
              </div>
              
              <div className="col-md-6">
                <label htmlFor="twitter_api_key" className="form-label">Twitter API Key</label>
                <input
                  type="password"
                  className="form-control"
                  id="twitter_api_key"
                  name="twitter_api_key"
                  value={settings.twitter_api_key}
                  onChange={handleInputChange}
                  placeholder="Enter your Twitter API key"
                />
              </div>
            </div>
          </div>
          
          <div className="mb-4">
            <h4>Lead Scoring Weights</h4>
            <p className="text-muted small">These weights determine how leads are scored. The sum should equal 1.0.</p>
            
            <div className="row mb-3">
              <div className="col-md-6">
                <label htmlFor="decision_maker_weight" className="form-label">Decision Maker Weight</label>
                <input
                  type="range"
                  className="form-range"
                  id="decision_maker_weight"
                  name="decision_maker_weight"
                  min="0"
                  max="1"
                  step="0.05"
                  value={settings.scoring.decision_maker_weight}
                  onChange={handleScoringChange}
                />
                <div className="d-flex justify-content-between">
                  <small>0</small>
                  <small>{settings.scoring.decision_maker_weight}</small>
                  <small>1</small>
                </div>
              </div>
              
              <div className="col-md-6">
                <label htmlFor="company_fit_weight" className="form-label">Company Fit Weight</label>
                <input
                  type="range"
                  className="form-range"
                  id="company_fit_weight"
                  name="company_fit_weight"
                  min="0"
                  max="1"
                  step="0.05"
                  value={settings.scoring.company_fit_weight}
                  onChange={handleScoringChange}
                />
                <div className="d-flex justify-content-between">
                  <small>0</small>
                  <small>{settings.scoring.company_fit_weight}</small>
                  <small>1</small>
                </div>
              </div>
            </div>
            
            <div className="row mb-3">
              <div className="col-md-6">
                <label htmlFor="growth_potential_weight" className="form-label">Growth Potential Weight</label>
                <input
                  type="range"
                  className="form-range"
                  id="growth_potential_weight"
                  name="growth_potential_weight"
                  min="0"
                  max="1"
                  step="0.05"
                  value={settings.scoring.growth_potential_weight}
                  onChange={handleScoringChange}
                />
                <div className="d-flex justify-content-between">
                  <small>0</small>
                  <small>{settings.scoring.growth_potential_weight}</small>
                  <small>1</small>
                </div>
              </div>
              
              <div className="col-md-6">
                <label htmlFor="skill_relevance_weight" className="form-label">Skill Relevance Weight</label>
                <input
                  type="range"
                  className="form-range"
                  id="skill_relevance_weight"
                  name="skill_relevance_weight"
                  min="0"
                  max="1"
                  step="0.05"
                  value={settings.scoring.skill_relevance_weight}
                  onChange={handleScoringChange}
                />
                <div className="d-flex justify-content-between">
                  <small>0</small>
                  <small>{settings.scoring.skill_relevance_weight}</small>
                  <small>1</small>
                </div>
              </div>
            </div>
            
            <div className="row mb-3">
              <div className="col-md-6">
                <label htmlFor="location_relevance_weight" className="form-label">Location Relevance Weight</label>
                <input
                  type="range"
                  className="form-range"
                  id="location_relevance_weight"
                  name="location_relevance_weight"
                  min="0"
                  max="1"
                  step="0.05"
                  value={settings.scoring.location_relevance_weight}
                  onChange={handleScoringChange}
                />
                <div className="d-flex justify-content-between">
                  <small>0</small>
                  <small>{settings.scoring.location_relevance_weight}</small>
                  <small>1</small>
                </div>
              </div>
              
              <div className="col-md-6">
                <label htmlFor="engagement_potential_weight" className="form-label">Engagement Potential Weight</label>
                <input
                  type="range"
                  className="form-range"
                  id="engagement_potential_weight"
                  name="engagement_potential_weight"
                  min="0"
                  max="1"
                  step="0.05"
                  value={settings.scoring.engagement_potential_weight}
                  onChange={handleScoringChange}
                />
                <div className="d-flex justify-content-between">
                  <small>0</small>
                  <small>{settings.scoring.engagement_potential_weight}</small>
                  <small>1</small>
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
                  Saving...
                </>
              ) : (
                <>
                  <i className="fas fa-save me-2"></i> Save Settings
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default SettingsPage; 