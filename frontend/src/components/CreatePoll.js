import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createPoll } from '../services/api';
import './CreatePoll.css';

const CreatePoll = () => {
  const [question, setQuestion] = useState('');
  const [options, setOptions] = useState(['', '']);
  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const navigate = useNavigate();

  const MAX_QUESTION_LENGTH = 200;

  const handleQuestionChange = (e) => {
    const value = e.target.value;
    if (value.length <= MAX_QUESTION_LENGTH) {
      setQuestion(value);
    }
  };

  const handleOptionChange = (index, value) => {
    const newOptions = [...options];
    newOptions[index] = value;
    setOptions(newOptions);
    // Clear error for this field when user starts typing
    if (errors[`option_${index}`]) {
      const newErrors = { ...errors };
      delete newErrors[`option_${index}`];
      setErrors(newErrors);
    }
  };

  const handleAddChoice = () => {
    setOptions([...options, '']);
  };

  const handleRemoveChoice = (index) => {
    if (options.length > 2) {
      const newOptions = options.filter((_, i) => i !== index);
      setOptions(newOptions);
    }
  };

  const validateForm = () => {
    const newErrors = {};

    // Validate question
    if (!question.trim()) {
      newErrors.question = 'Poll question is required';
    } else if (question.trim().length < 3) {
      newErrors.question = 'Question must be at least 3 characters';
    }

    // Validate options (at least 2 non-empty)
    const validOptions = options.filter(opt => opt.trim().length > 0);
    if (validOptions.length < 2) {
      newErrors.options = 'At least 2 options are required';
    }

    // Validate individual options
    options.forEach((opt, index) => {
      if (opt.trim().length === 0 && index < 2) {
        newErrors[`option_${index}`] = 'This option is required';
      }
    });

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setIsSubmitting(true);

    try {
      // Filter out empty options
      const validOptions = options.filter(opt => opt.trim().length > 0);
      
      const response = await createPoll(question.trim(), validOptions);
      
      // Navigate to poll view
      navigate(`/poll/${response.poll_link}`);
    } catch (error) {
      console.error('Error creating poll:', error);
      setErrors({
        submit: error.response?.data?.error || 'Failed to create poll. Please try again.',
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="create-poll-container">
      <div className="create-poll-card">
        <h1 className="create-poll-title">Create a New Poll</h1>
        
        <form onSubmit={handleSubmit} className="create-poll-form">
          {/* Poll Question Section */}
          <div className="form-section">
            <label htmlFor="question" className="form-label">
              Poll Question
            </label>
            <textarea
              id="question"
              className={`form-textarea ${errors.question ? 'error' : ''}`}
              placeholder="what is ..."
              value={question}
              onChange={handleQuestionChange}
              rows={4}
            />
            <div className="form-footer">
              <span className="error-message">{errors.question}</span>
              <span className="char-counter">
                {question.length} / {MAX_QUESTION_LENGTH}
              </span>
            </div>
          </div>

          {/* Poll Choices Section */}
          <div className="form-section">
            <label className="form-label">Poll Choices</label>
            {options.map((option, index) => (
              <div key={index} className="option-input-wrapper">
                <input
                  type="text"
                  className={`form-input ${errors[`option_${index}`] ? 'error' : ''}`}
                  placeholder={`Choice ${index + 1}`}
                  value={option}
                  onChange={(e) => handleOptionChange(index, e.target.value)}
                />
                {options.length > 2 && (
                  <button
                    type="button"
                    className="remove-choice-btn"
                    onClick={() => handleRemoveChoice(index)}
                    aria-label="Remove choice"
                  >
                    ×
                  </button>
                )}
                {errors[`option_${index}`] && (
                  <span className="error-message inline-error">
                    {errors[`option_${index}`]}
                  </span>
                )}
              </div>
            ))}
            
            {errors.options && (
              <span className="error-message">{errors.options}</span>
            )}
            
            <button
              type="button"
              className="add-choice-btn"
              onClick={handleAddChoice}
            >
              <span className="add-icon">+</span> Add Choice
            </button>
          </div>

          {/* Submit Error */}
          {errors.submit && (
            <div className="error-message submit-error">{errors.submit}</div>
          )}

          {/* Create Poll Button */}
          <button
            type="submit"
            className="create-poll-btn"
            disabled={isSubmitting}
          >
            {isSubmitting ? 'Creating...' : 'Create Poll'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default CreatePoll;

