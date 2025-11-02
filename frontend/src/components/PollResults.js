import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getPollResults } from '../services/api';
import './PollResults.css';

const PollResults = () => {
  const { pollLink } = useParams();
  const navigate = useNavigate();
  const [poll, setPoll] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchResults();
    // Refresh results every 5 seconds
    const interval = setInterval(fetchResults, 5000);
    return () => clearInterval(interval);
  }, [pollLink]);

  const fetchResults = async () => {
    try {
      setIsLoading(true);
      const response = await getPollResults(pollLink);
      setPoll(response.poll);
      setError(null);
    } catch (err) {
      console.error('Error fetching results:', err);
      setError(err.response?.data?.error || 'Failed to load results');
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading && !poll) {
    return (
      <div className="poll-results-container">
        <div className="poll-card">
          <div className="loading-message">Loading results...</div>
        </div>
      </div>
    );
  }

  if (error && !poll) {
    return (
      <div className="poll-results-container">
        <div className="poll-card">
          <div className="error-message">{error}</div>
          <button className="btn-primary" onClick={() => navigate('/')}>
            Create New Poll
          </button>
        </div>
      </div>
    );
  }

  if (!poll) {
    return null;
  }

  const maxVotes = Math.max(...poll.options.map(opt => opt.vote_count), 1);

  return (
    <div className="poll-results-container">
      <div className="poll-card">
        <h1 className="poll-question">{poll.question}</h1>
        
        <div className="results-summary">
          <span className="total-votes">
            {poll.total_votes} {poll.total_votes === 1 ? 'vote' : 'votes'}
          </span>
        </div>

        <div className="results-list">
          {poll.options.map((option) => {
            const percentage = option.percentage || 0;
            const width = maxVotes > 0 ? (option.vote_count / maxVotes) * 100 : 0;

            return (
              <div key={option.option_id} className="result-item">
                <div className="result-header">
                  <span className="result-option-text">{option.option_text}</span>
                  <span className="result-stats">
                    {option.vote_count} ({percentage}%)
                  </span>
                </div>
                <div className="result-bar-container">
                  <div
                    className="result-bar"
                    style={{ width: `${width}%` }}
                  >
                    <div className="result-bar-fill" />
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {poll.total_votes === 0 && (
          <div className="no-votes-message">
            No votes yet. Be the first to vote!
          </div>
        )}

        <div className="poll-actions">
          <button
            className="btn-secondary"
            onClick={() => navigate(`/poll/${pollLink}`)}
          >
            Vote Again
          </button>
          <button className="btn-primary" onClick={() => navigate('/')}>
            Create New Poll
          </button>
        </div>

        <div className="poll-link-section">
          <p className="share-text">Share this poll:</p>
          <div className="poll-link-container">
            <input
              type="text"
              readOnly
              value={window.location.origin + `/poll/${pollLink}`}
              className="poll-link-input"
              onClick={(e) => e.target.select()}
            />
            <button
              className="copy-btn"
              onClick={() => {
                navigator.clipboard.writeText(window.location.origin + `/poll/${pollLink}`);
                alert('Link copied to clipboard!');
              }}
            >
              Copy
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PollResults;

