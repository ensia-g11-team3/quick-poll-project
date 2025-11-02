# Quick Poll App - Frontend

React.js frontend for the Quick Poll App.

## 📋 Overview

The frontend is built with React 18.2 and provides a modern, responsive user interface for creating polls, voting, and viewing results.

## 🚀 Quick Start

### Installation

1. **Install dependencies:**
```bash
npm install
```

2. **Start development server:**
```bash
npm start
```

The app will automatically open at `http://localhost:3000`

### Configuration

Create a `.env` file in the frontend directory if you need to change the API URL:
```bash
REACT_APP_API_URL=http://localhost:5000/api
```

## 📁 Project Structure

```
frontend/
├── public/
│   └── index.html          # HTML template
├── src/
│   ├── components/         # React components
│   │   ├── CreatePoll.js   # Poll creation form
│   │   ├── CreatePoll.css  # Styling for create poll
│   │   ├── PollView.js     # Voting interface
│   │   ├── PollView.css    # Styling for poll view
│   │   ├── PollResults.js  # Results display
│   │   └── PollResults.css # Styling for results
│   ├── services/
│   │   └── api.js          # API client functions
│   ├── App.js              # Main app component with routing
│   ├── App.css             # App-level styles
│   ├── index.js            # Application entry point
│   └── index.css           # Global styles
├── package.json            # Dependencies and scripts
└── README.md              # This file
```

## 🎨 Components

### CreatePoll
- **Purpose**: Create new polls with questions and options
- **Features**:
  - Question input (200 character limit)
  - Dynamic option fields (minimum 2)
  - Add/remove options
  - Form validation
  - Character counter

### PollView
- **Purpose**: Display poll and allow voting
- **Features**:
  - Radio button selection
  - Submit vote functionality
  - View results button
  - Share link functionality
  - Copy link to clipboard

### PollResults
- **Purpose**: Display poll results
- **Features**:
  - Vote counts per option
  - Percentage calculations
  - Visual progress bars
  - Auto-refresh every 5 seconds
  - Share functionality

## 🔧 Available Scripts

### `npm start`
Runs the app in development mode at `http://localhost:3000`
- Hot reload enabled
- Opens browser automatically
- Shows compilation errors

### `npm build`
Builds the app for production to the `build` folder
- Optimized for performance
- Minified files
- Ready for deployment

### `npm test`
Launches the test runner (not configured in this project)

### `npm eject`
**One-way operation** - Ejects from Create React App (not recommended)

## 🎯 Features

- ✅ **Poll Creation**: Easy-to-use form with dynamic options
- ✅ **Voting System**: Simple radio button selection
- ✅ **Real-time Results**: Live vote counts and percentages
- ✅ **Share Links**: Copy poll links to clipboard
- ✅ **Responsive Design**: Works on desktop, tablet, and mobile
- ✅ **Form Validation**: Client-side validation for better UX
- ✅ **Error Handling**: User-friendly error messages

## 🛠 Technologies

- **React 18.2.0** - UI library
- **React Router 6.20.0** - Client-side routing
- **Axios 1.6.2** - HTTP client
- **CSS3** - Styling with modern features

## 📱 Responsive Design

The app is fully responsive with:
- Mobile-first approach
- Breakpoints for tablets and desktops
- Touch-friendly buttons
- Optimized layouts for all screen sizes

## 🔌 API Integration

The frontend communicates with the backend via the `api.js` service layer:

```javascript
// Example usage
import { createPoll, getPoll, submitVote } from './services/api';

// Create poll
const response = await createPoll(question, options);

// Get poll
const poll = await getPoll(pollLink);

// Submit vote
await submitVote(pollId, optionId);
```

## 🎨 Styling

- Custom CSS with CSS modules
- Purple gradient theme
- Modern card-based layout
- Smooth animations and transitions
- Consistent color scheme

## 🐛 Troubleshooting

### Port 3000 already in use
React will prompt to use a different port, or:
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Module not found errors
```bash
rm -rf node_modules package-lock.json
npm install
```

### API connection errors
- Ensure backend is running on port 5000
- Check `REACT_APP_API_URL` in `.env`
- Verify CORS settings in backend

### Build errors
```bash
npm cache clean --force
npm install
```

## 📦 Dependencies

See `package.json` for complete list. Main dependencies:
- react: ^18.2.0
- react-dom: ^18.2.0
- react-router-dom: ^6.20.0
- axios: ^1.6.2
- react-scripts: 5.0.1

## 🔄 Development Workflow

1. Start backend server (port 5000)
2. Start frontend server: `npm start`
3. Make changes to components
4. See changes reflected immediately (hot reload)
5. Check browser console for errors (F12)

## 📝 Notes

- The app uses React Router for navigation
- All API calls are handled through the service layer
- Local storage is used for tracking voted polls
- No state management library (Redux/MobX) needed for this scope

For more information, see the main [README.md](../README.md)

