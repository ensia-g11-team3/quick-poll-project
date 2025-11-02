import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Poll API
export const createPoll = async (question, options, creatorId = null) => {
  const response = await api.post('/polls', {
    question,
    options,
    creator_id: creatorId,
  });
  return response.data;
};

export const getPoll = async (pollLink) => {
  const response = await api.get(`/polls/${pollLink}`);
  return response.data;
};

export const getPollResults = async (pollLink) => {
  const response = await api.get(`/polls/${pollLink}/results`);
  return response.data;
};

// Vote API
export const submitVote = async (pollId, optionId, voterId = null) => {
  const response = await api.post('/votes', {
    poll_id: pollId,
    option_id: optionId,
    voter_id: voterId,
  });
  return response.data;
};

// User API
export const registerUser = async (username, email, password) => {
  const response = await api.post('/users/register', {
    username,
    email,
    password,
  });
  return response.data;
};

export const loginUser = async (email, password) => {
  const response = await api.post('/users/login', {
    email,
    password,
  });
  return response.data;
};

export default api;

