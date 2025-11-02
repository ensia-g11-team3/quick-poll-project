import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getPoll, submitVote } from '../services/api';
import './PollView.css';

const PollView = () => {
  const { pollLink } = useParams();
  const navigate = useNavigate();
  const [poll, setPoll] = useState(null);
  const [selectedOption, setSelectedOption] = useState(null);
  const [hasVoted, setHasVoted] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchPoll();
  }, [pollLink]);

  const fetchPoll = async () => {
    try {
      setIsLoading(true);
      const response = await getPoll(pollLink);
      setPoll(response.poll);
      
      // Check if already voted (could be stored in localStorage or cookie)
      const votedPolls = JSON.parse(localStorage.getItem('votedPolls') || '{}');
      if (votedPolls[pollLink]) {
        setHasVoted(true);
        setSelectedOption(votedPolls[pollLink]);
      }
    } catch (err) {
      console.error('Error fetching poll:', err);
      setError(err.response?.data?.error || 'Failed to load poll');
    } finally {
      setIsLoading(false);
    }
  };

  const handleVote = async () => {
    if (!selectedOption) {
      setError('Please select an option');
      return;
    }

    setIsSubmitting(true);
    setError(null);

    try {
      await submitVote(poll.poll_id, selectedOption);
      
      // Store vote in localStorage to prevent duplicate votes
      const votedPolls = JSON.parse(localStorage.getItem('votedPolls') || '{}');
      votedPolls[pollLink] = selectedOption;
      localStorage.setItem('votedPolls', JSON.stringify(votedPolls));
      
      setHasVoted(true);
      // Navigate to results page
      navigate(`/poll/${pollLink}/results`);
    } catch (err) {
      console.error('Error submitting vote:', err);
      setError(err.response?.data?.error || 'Failed to submit vote. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleViewResults = () => {
    navigate(`/poll/${pollLink}/results`);
  };

  if (isLoading) {
    return (
      <div className="poll-view-container">
        <div className="poll-card">
          <div className="loading-message">Loading poll...</div>
        </div>
      </div>
    );
  }

  if (error && !poll) {
    return (
      <div className="poll-view-container">
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

  return (
    <div className="poll-view-container">
      <div className="poll-card">
        <h1 className="poll-question">{poll.question}</h1>
        
        {error && (
          <div className="error-message submit-error">{error}</div>
        )}

        <div className="poll-options">
          {poll.options.map((option) => (
            <label
              key={option.option_id}
              className={`poll-option ${selectedOption === option.option_id ? 'selected' : ''} ${hasVoted ? 'disabled' : ''}`}
            >
              <input
                type="radio"
                name="poll-option"
                value={option.option_id}
                checked={selectedOption === option.option_id}
                onChange={() => setSelectedOption(option.option_id)}
                disabled={hasVoted}
              />
              <span className="option-text">{option.option_text}</span>
            </label>
          ))}
        </div>

        {!hasVoted ? (
          <div className="poll-actions">
            <button
              className="btn-primary"
              onClick={handleVote}
              disabled={!selectedOption || isSubmitting}
            >
              {isSubmitting ? 'Submitting...' : 'Submit Vote'}
            </button>
            <button
              className="btn-secondary"
              onClick={handleViewResults}
            >
              View Results
            </button>
          </div>
        ) : (
          <div className="poll-actions">
            <button className="btn-primary" onClick={handleViewResults}>
              View Results
            </button>
            <button className="btn-secondary" onClick={() => navigate('/')}>
              Create New Poll
            </button>
          </div>
        )}

        <div className="poll-link-section">
          <p className="share-text">Share this poll:</p>
          <div className="poll-link-container">
            <input
              type="text"
              readOnly
              value={window.location.href}
              className="poll-link-input"
              onClick={(e) => e.target.select()}
            />
            <button
              className="copy-btn"
              onClick={() => {
                navigator.clipboard.writeText(window.location.href);
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

export default PollView;

